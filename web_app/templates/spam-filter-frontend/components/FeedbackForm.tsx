"use client";

import React, { useState } from "react";

interface FeedbackFormProps {
  emailBody: string;
  predictedLabel: string;
}

export default function FeedbackForm({ emailBody, predictedLabel }: FeedbackFormProps) {
  const [feedback, setFeedback] = useState<"correct" | "incorrect" | "">("");
  const [message, setMessage] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const [showToast, setShowToast] = useState(false);

  const API_BASE = "http://localhost:5000";

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!feedback) {
      alert("Pilih feedback terlebih dahulu");
      return;
    }
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/feedback`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: emailBody,
          predicted_label: predictedLabel,
          feedback,
        }),
      });
      const data = await res.json();
      if (data.success) {
        setMessage(data.message);
        setFeedback("");
        setIsOpen(false);
        setShowToast(true);
        setTimeout(() => setShowToast(false), 3000); // Hide toast after 3 seconds
      } else {
        setMessage("Gagal mengirim feedback: " + data.message);
      }
    } catch (error) {
      setMessage("Terjadi kesalahan saat mengirim feedback.");
    }
    setLoading(false);
  }

  return (
    <>
      {/* Toast Notification */}
      {showToast && (
        <div className="fixed top-4 right-4 bg-green-500 text-white px-4 py-2 rounded shadow z-50 animate-fade-in-out">
          {message}
        </div>
      )}

      <button
        onClick={() => setIsOpen(true)}
        className="px-4 py-2 bg-indigo-600 text-white rounded shadow hover:bg-indigo-500"
      >
        Beri Feedback
      </button>

      {isOpen && (
        <div className="fixed inset-0 z-40 flex items-center justify-center bg-black/50">
          <div className="bg-white rounded-lg shadow-lg p-6 w-full max-w-md relative">
            <button
              onClick={() => setIsOpen(false)}
              className="absolute top-2 right-2 text-gray-500 hover:text-red-500 text-xl font-bold"
            >
              &times;
            </button>
            <h2 className="text-lg font-semibold mb-4">Feedback Prediksi</h2>
            <form onSubmit={handleSubmit}>
              <div className="mb-4">
                <label className="block">
                  <input
                    type="radio"
                    name="feedback"
                    value="correct"
                    checked={feedback === "correct"}
                    onChange={() => setFeedback("correct")}
                    disabled={loading}
                  />
                  <span className="ml-2">Prediksi benar</span>
                </label>
                <label className="block mt-2">
                  <input
                    type="radio"
                    name="feedback"
                    value="incorrect"
                    checked={feedback === "incorrect"}
                    onChange={() => setFeedback("incorrect")}
                    disabled={loading}
                  />
                  <span className="ml-2">Prediksi salah</span>
                </label>
              </div>
              <button
                type="submit"
                disabled={loading}
                className="w-full px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-500"
              >
                {loading ? "Mengirim..." : "Kirim Feedback"}
              </button>
            </form>
          </div>
        </div>
      )}
    </>
  );
}
