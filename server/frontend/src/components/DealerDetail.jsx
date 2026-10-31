import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import { apiRequest } from "../api";
import { useAuth } from "../auth";

export default function DealerDetail() {
  const { dealerId } = useParams();
  const { user } = useAuth();
  const [dealer, setDealer] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [carModels, setCarModels] = useState([]);
  const [text, setText] = useState("");
  const [purchase, setPurchase] = useState(false);
  const [purchaseDate, setPurchaseDate] = useState("");
  const [carMake, setCarMake] = useState("");
  const [carModel, setCarModel] = useState("");
  const [carYear, setCarYear] = useState("");
  const [sentiment, setSentiment] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function loadDetails() {
    const [dealerData, reviewData, carModelsData] = await Promise.all([
      apiRequest(`/getdealerbyid/${dealerId}/`),
      apiRequest(`/getdealerreviews/${dealerId}/`),
      apiRequest("/djangoapp/get_cars"),
    ]);
    setDealer(dealerData);
    setReviews(reviewData);
    setCarModels(carModelsData.CarModels);
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
        body: JSON.stringify({
          text,
          purchase,
          purchase_date: purchase ? purchaseDate : null,
          car_make: purchase ? carMake : "",
          car_model: purchase ? carModel : "",
          car_year: purchase && carYear ? Number(carYear) : null,
        }),
      });
      setSentiment("");
      setText("");
      setPurchase(false);
      setPurchaseDate("");
      setCarMake("");
      setCarModel("");
      setCarYear("");
      setMessage("Thanks — your review has been added.");
      await loadDetails();
      try {
        const analysis = await apiRequest("/analyzereview/", {
          method: "POST",
          body: JSON.stringify({ review: text }),
        });
        setSentiment(analysis.sentiment);
      } catch (analysisError) {
        setError(`Your review was posted, but sentiment analysis failed: ${analysisError.message}`);
      }
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
              {review.purchase && (
                <p className="review-purchase">
                  Purchased {review.car_year} {review.car_make} {review.car_model}
                  {review.purchase_date ? ` on ${review.purchase_date}` : ""}
                </p>
              )}
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
            <label className="purchase-toggle">
              <input
                type="checkbox"
                checked={purchase}
                onChange={(event) => setPurchase(event.target.checked)}
              />
              I purchased a vehicle from this dealership
            </label>
            {purchase && (
              <div className="purchase-fields">
                <label htmlFor="purchase-date">Purchase date</label>
                <input
                  id="purchase-date"
                  type="date"
                  required
                  value={purchaseDate}
                  onChange={(event) => setPurchaseDate(event.target.value)}
                />
                <label htmlFor="car-make">Car make</label>
                <select
                  id="car-make"
                  required
                  value={carMake}
                  onChange={(event) => {
                    setCarMake(event.target.value);
                    setCarModel("");
                  }}
                >
                  <option value="">Select a make</option>
                  {[...new Set(carModels.map((car) => car.CarMake))].map((make) => (
                    <option key={make} value={make}>{make}</option>
                  ))}
                </select>
                <label htmlFor="car-model">Car model</label>
                <select
                  id="car-model"
                  required
                  disabled={!carMake}
                  value={carModel}
                  onChange={(event) => setCarModel(event.target.value)}
                >
                  <option value="">Select a model</option>
                  {carModels
                    .filter((car) => car.CarMake === carMake)
                    .map((car) => (
                      <option key={car.CarModel} value={car.CarModel}>{car.CarModel}</option>
                    ))}
                </select>
                <label htmlFor="car-year">Car year</label>
                <input
                  id="car-year"
                  type="number"
                  min="1886"
                  max={new Date().getFullYear() + 1}
                  required
                  value={carYear}
                  onChange={(event) => setCarYear(event.target.value)}
                />
              </div>
            )}
            {message && <p className="notice success" role="status">{message}</p>}
            {error && <p className="notice error" role="alert">{error}</p>}
            {sentiment && (
              <p className="review-sentiment" role="img" aria-label={`${sentiment} sentiment`}>
                {sentiment === "positive" ? "😊" : sentiment === "negative" ? "☹️" : "😐"}
                <span>{sentiment} sentiment</span>
              </p>
            )}
            <button className="button" type="submit">Post review</button>
          </form>
        ) : (
          <p className="notice">Please <Link to="/login">log in</Link> to leave a review.</p>
        )}
      </section>
    </main>
  );
}
