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
      } else {
        setMessage("Gagal mengirim feedback: " + data.message);
      }
    } catch (error) {
      setMessage("Terjadi kesalahan saat mengirim feedback.");
    }
    setLoading(false);
  }

  return (
    <form onSubmit={handleSubmit} style={{ marginTop: 10 }}>
      <label>
        <input
          type="radio"
          name="feedback"
          value="correct"
          checked={feedback === "correct"}
          onChange={() => setFeedback("correct")}
          disabled={loading}
        />
        Prediksi benar
      </label>
      <label style={{ marginLeft: 10 }}>
        <input
          type="radio"
          name="feedback"
          value="incorrect"
          checked={feedback === "incorrect"}
          onChange={() => setFeedback("incorrect")}
          disabled={loading}
        />
        Prediksi salah
      </label>
      <button type="submit" className="px-2 py-1 bg-blue-600 text-white rounded-md shadow transition-all hover:bg-blue-500 hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-blue-400 sm:mt-10 sm:ml-20" disabled={loading}>
        {loading ? "Mengirim..." : "Kirim Feedback"}
      </button>
      {message && <p style={{ marginTop: 10 }}>{message}</p>}
    </form>
  );
}
