import { notFound } from "next/navigation";
import { Email } from "../../type";
import FeedbackForm from "../../../components/FeedbackForm";

function slugify(text: string) {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)+/g, "");
}

function createSlug(email: Email) {
  return `${slugify(email.subject)}-${email.subject.length}`;
}

async function getEmailBySlug(slug: string): Promise<Email | null> {
  try {
    const res = await fetch(`http://localhost:5000/emails?page=1&filter=all`, {
      cache: "no-store",
    });
    const data = await res.json();
    if (!data.success) return null;

    const emails: Email[] = data.emails;
    const found = emails.find((email) => createSlug(email) === slug);
    return found || null;
  } catch (err) {
    console.error(err);
    return null;
  }
}

export default async function EmailDetailPage({ params }: { params: { slug: string } }) {
  const email = await getEmailBySlug(params.slug);
  if (!email) return notFound();

  return (
    <section className="max-w-3xl mx-auto px-6 py-10 text-gray-800">
      <div className="bg-white shadow-lg rounded-2xl p-8 border border-gray-100">
        <h1 className="text-2xl sm:text-3xl font-bold mb-4">{email.subject}</h1>

        <div className="flex flex-wrap gap-4 text-sm mb-6">
          <span className="inline-block bg-blue-100 text-blue-700 px-3 py-1 rounded-full font-medium">
            {email.label}
          </span>
          <span className="text-gray-500">Confidence: <span className="font-semibold">{email.confidence.toFixed(2)}</span></span>
        </div>

        <hr className="my-4" />

        <article className="prose prose-sm sm:prose lg:prose-lg max-w-none text-gray-900 whitespace-pre-line">
          {email.body}
        </article>

        <div className="mt-10 pt-6 border-t border-gray-200">
          <h2 className="text-lg font-semibold mb-4 text-gray-700">Berikan Feedback Anda</h2>
          <div className="w-full">
            <FeedbackForm emailBody={email.body} predictedLabel={email.label} />
          </div>
        </div>
      </div>
    </section>
  );
}
