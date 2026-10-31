import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import { apiRequest } from "../api";
import { useAuth } from "../auth";

export default function DealerDetail() {
  const { dealerId } = useParams();
  const { user } = useAuth();
  const [dealer, setDealer] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [text, setText] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function loadDetails() {
    const [dealerData, reviewData] = await Promise.all([
      apiRequest(`/getdealerbyid/${dealerId}/`),
      apiRequest(`/getdealerreviews/${dealerId}/`),
    ]);
    setDealer(dealerData);
    setReviews(reviewData);
  }

  useEffect(() => {
    loadDetails().catch((requestError) => setError(requestError.message));
  }, [dealerId]);

  async function submitReview(event) {
    event.preventDefault();
    setError("");
    setMessage("");
    try {
      await apiRequest(`/dealers/${dealerId}/reviews/`, {
        method: "POST",
        token: user?.token,
        body: JSON.stringify({ text }),
      });
      setText("");
      setMessage("Thanks — your review has been added.");
      await loadDetails();
    } catch (requestError) {
      setError(requestError.message);
    }
  }

  if (error && !dealer) return <main className="content-page"><p role="alert">{error}</p></main>;
  if (!dealer) return <main className="content-page"><p role="status">Loading dealership…</p></main>;

  return (
    <main className="content-page">
      <Link className="back-link" to="/">← All dealerships</Link>
      <section className="detail-hero">
        <p className="eyebrow">{dealer.city}, {dealer.state}</p>
        <h1>{dealer.name}</h1>
        <p>{dealer.description}</p>
        <div className="detail-meta"><span>{dealer.address}</span><span>{dealer.phone}</span></div>
      </section>
      <section className="reviews-section">
        <div className="section-heading">
          <div><p className="eyebrow">CUSTOMER STORIES</p><h2>Reviews</h2></div>
          <span>{reviews.length} {reviews.length === 1 ? "review" : "reviews"}</span>
        </div>
        {reviews.map((review) => (
          <article className="review-card" key={review.id}>
            <div className="review-avatar">{review.reviewer.slice(0, 1).toUpperCase()}</div>
            <div><strong>{review.reviewer}</strong><p>{review.text}</p>
              <time dateTime={review.created_at}>{new Date(review.created_at).toLocaleDateString()}</time>
            </div>
          </article>
        ))}
        {reviews.length === 0 && <p className="notice">Be the first to share your experience.</p>}
        {user ? (
          <form className="review-form" onSubmit={submitReview}>
            <h3>Share your experience</h3>
            <label htmlFor="review-text">Your review</label>
            <textarea id="review-text" required maxLength={2000} value={text} onChange={(event) => setText(event.target.value)} />
            {message && <p className="notice success" role="status">{message}</p>}
            {error && <p className="notice error" role="alert">{error}</p>}
            <button className="button" type="submit">Post review</button>
          </form>
        ) : (
          <p className="notice">Please <Link to="/login">log in</Link> to leave a review.</p>
        )}
      </section>
    </main>
  );
}
