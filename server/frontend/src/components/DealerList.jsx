import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { apiRequest } from "../api";

export default function DealerList() {
  const [dealers, setDealers] = useState([]);
  const [state, setState] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;
    setLoading(true);
    setError("");
    const path = state
      ? `/getdealersbystate/${encodeURIComponent(state)}/`
      : "/getalldealers/";
    apiRequest(path)
      .then((data) => active && setDealers(data))
      .catch((requestError) => active && setError(requestError.message))
      .finally(() => active && setLoading(false));
    return () => {
      active = false;
    };
  }, [state]);

  return (
    <main>
      <section className="hero">
        <div className="hero-copy">
          <p className="eyebrow">YOUR NEXT CHAPTER STARTS HERE</p>
          <h1>Find a car dealer<br />you can <em>feel good</em> about.</h1>
          <p className="hero-subtitle">
            Browse trusted local dealerships, explore their inventory, and hear
            from real customers.
          </p>
          <a className="button" href="#dealers">Explore dealerships <span aria-hidden="true">↓</span></a>
        </div>
        <div className="hero-art" aria-label="Illustration of a car on a scenic road">
          <div className="sun" />
          <div className="hill hill-back" />
          <div className="hill hill-front" />
          <div className="road" />
          <div className="hero-car"><span /><i /><b /></div>
          <div className="art-caption">THE ROAD AHEAD IS YOURS</div>
        </div>
      </section>

      <section className="dealer-section" id="dealers">
        <div className="section-heading">
          <div>
            <p className="eyebrow">OUR DEALER NETWORK</p>
            <h2>Good people. Great drives.</h2>
          </div>
          <label className="filter-label">
            Filter by state
            <select aria-label="Filter by state" value={state} onChange={(event) => setState(event.target.value)}>
              <option value="">All states</option>
              <option value="KS">Kansas</option>
              <option value="AZ">Arizona</option>
              <option value="CO">Colorado</option>
              <option value="IL">Illinois</option>
            </select>
          </label>
        </div>
        {loading && <p role="status">Loading dealerships…</p>}
        {error && <p className="notice error" role="alert">{error}</p>}
        {!loading && !error && dealers.length === 0 && (
          <p className="notice">No dealerships found in this state yet.</p>
        )}
        <div className="dealer-grid">
          {dealers.map((dealer) => (
            <article className="dealer-card" key={dealer.id}>
              <div className="card-icon" aria-hidden="true">⌖</div>
              <p className="dealer-location">{dealer.city}, {dealer.state}</p>
              <h3>{dealer.name}</h3>
              <p className="card-description">{dealer.description}</p>
              <Link className="text-link" to={`/dealers/${dealer.id}`}>
                View dealership <span aria-hidden="true">→</span>
              </Link>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}
