"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { Email } from "../type";
import FeedbackForm from "../../components/FeedbackForm";

function slugify(text: string) {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)+/g, "");
}

export default function EmailListPage() {
  const [emails, setEmails] = useState<Email[]>([]);
  const [page, setPage] = useState<number>(1);
  const [filter, setFilter] = useState<string>("all");
  const [hasNext, setHasNext] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(false);
  const API_BASE = "http://localhost:5000";

  async function fetchEmails() {
    setLoading(true);
    try {
      const res = await fetch(
        `${API_BASE}/emails?page=${page}&filter=${filter}`,
        { cache: "no-store" }
      );
      const data = await res.json();
      if (data.success) {
        setEmails(data.emails);
        setHasNext(data.has_next);
      } else {
        alert("Gagal load emails: " + data.message);
      }
    } catch (error) {
      alert("Error fetch emails");
    }
    setLoading(false);
  }

  useEffect(() => {
    fetchEmails();
  }, [page, filter]);

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 text-gray-800">
      <h1 className="text-3xl font-semibold mb-6 text-center">📨 Email Spam Filter</h1>

      <div className="flex justify-between items-center mb-6">
        <label className="text-sm font-medium mr-2">Filter:</label>
        <select
          value={filter}
          onChange={(e) => {
            setPage(1);
            setFilter(e.target.value);
          }}
          className="border rounded px-3 py-1 text-sm"
        >
          <option value="all">All</option>
          <option value="spam">Spam</option>
          <option value="ham">Ham</option>
        </select>
      </div>

      {loading ? (
        <p className="text-center text-gray-500">Loading emails...</p>
      ) : (
        <ul className="space-y-4">
          {emails.map((email) => {
            const slug = slugify(email.subject);
            const slugId = encodeURIComponent(`${slug}-${email.subject.length}`);

            return (
              <li
                key={slug}
                className="bg-white rounded-xl shadow hover:shadow-md transition-shadow border border-gray-200 p-4"
              >
                <Link href={`/emails/${slugId}`}>
                  <span className="text-lg font-semibold text-blue-600 cursor-pointer hover:underline">
                    {email.subject}
                  </span>
                </Link>
                <div className="text-sm text-gray-600 mt-1 mb-2">
                  <span className={`px-2 py-0.5 rounded-full text-xs font-semibold mr-2 
                  ${
                    email.label === "SPAM"
                        ? "bg-red-600 text-white border border-red-700" 
                        : "bg-green-100 text-green-600"
                    }`}>
                    {email.label}
                </span>
                  Confidence: {email.confidence.toFixed(2)}
                </div>
                <p className="text-sm text-gray-700">{email.preview}</p>

                <div className="mt-3">
                  <FeedbackForm
                    key={email.body}
                    emailBody={email.body}
                    predictedLabel={email.label}
                  />
                </div>
              </li>
            );
          })}
        </ul>
      )}

      <div className="mt-8 flex justify-center items-center space-x-4">
        <button
          disabled={page === 1}
          onClick={() => setPage(page - 1)}
          className="bg-gray-200 hover:bg-gray-300 px-4 py-1 rounded disabled:opacity-50"
        >
          Prev
        </button>
        <span className="text-sm">Page {page}</span>
        <button
          disabled={!hasNext}
          onClick={() => setPage(page + 1)}
          className="bg-gray-200 hover:bg-gray-300 px-4 py-1 rounded disabled:opacity-50"
        >
          Next
        </button>
      </div>
    </div>
  );
}
