import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { BrowserRouter } from "react-router-dom";
import { beforeEach, describe, expect, it, vi } from "vitest";

import App from "./App.jsx";
import { AuthProvider } from "./auth.jsx";

const dealer = {
  id: 1,
  name: "Heartland Motors",
  city: "Wichita",
  state: "KS",
  address: "1200 E Douglas Ave",
  phone: "316-555-0142",
  description: "A neighborhood dealership.",
};

function jsonResponse(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

function renderAt(path) {
  window.history.pushState({}, "", path);
  return render(
    <BrowserRouter>
      <AuthProvider><App /></AuthProvider>
    </BrowserRouter>,
  );
}

describe("account and review flows", () => {
  beforeEach(() => {
    localStorage.clear();
    vi.restoreAllMocks();
  });

  it("registers an account and establishes the authenticated state", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch")
      .mockResolvedValueOnce(jsonResponse({ token: "registered-token", username: "new-customer" }, 201))
      .mockResolvedValueOnce(jsonResponse([]))
      .mockResolvedValueOnce(jsonResponse([]));
    const user = userEvent.setup();
    renderAt("/register");

    await user.type(screen.getByLabelText("Username"), "new-customer");
    await user.type(screen.getByLabelText("First Name"), "New");
    await user.type(screen.getByLabelText("Last Name"), "Customer");
    await user.type(screen.getByLabelText("Email"), "new@example.test");
    await user.type(screen.getByLabelText("Password"), "Distinctive-passphrase-72!");
    await user.type(screen.getByLabelText("Confirm password"), "Distinctive-passphrase-72!");
    await user.click(screen.getByRole("button", { name: "Register" }));

    expect(await screen.findByText("Hi, new-customer")).toBeInTheDocument();
    expect(JSON.parse(localStorage.getItem("dealershipUser")).token).toBe("registered-token");
    expect(JSON.parse(fetchMock.mock.calls[0][1].body)).toMatchObject({
      username: "new-customer",
      first_name: "New",
      last_name: "Customer",
      email: "new@example.test",
    });
  });

  it("rejects mismatched registration passwords without calling the API", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch");
    const user = userEvent.setup();
    renderAt("/register");

    await user.type(screen.getByLabelText("Username"), "new-customer");
    await user.type(screen.getByLabelText("First Name"), "New");
    await user.type(screen.getByLabelText("Last Name"), "Customer");
    await user.type(screen.getByLabelText("Email"), "new@example.test");
    await user.type(screen.getByLabelText("Password"), "Distinctive-passphrase-72!");
    await user.type(screen.getByLabelText("Confirm password"), "Different-passphrase-72!");
    await user.click(screen.getByRole("button", { name: "Register" }));

    expect(await screen.findByRole("alert")).toHaveTextContent("Passwords do not match.");
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("logs in and logs out through the token API", async () => {
    vi.spyOn(globalThis, "fetch")
      .mockResolvedValueOnce(jsonResponse({ token: "login-token", username: "returning-user" }))
      .mockResolvedValueOnce(jsonResponse([]))
      .mockResolvedValueOnce(jsonResponse({ message: "Logged out successfully." }))
      .mockResolvedValueOnce(jsonResponse([]));
    const user = userEvent.setup();
    renderAt("/login");

    await user.type(screen.getByLabelText("Username"), "returning-user");
    await user.type(screen.getByLabelText("Password"), "any-password");
    await user.click(screen.getByRole("button", { name: "Log in" }));
    expect(await screen.findByText("Hi, returning-user")).toBeInTheDocument();

    await user.click(screen.getByRole("button", { name: "Log out" }));
    expect(await screen.findByRole("link", { name: "Log in" })).toBeInTheDocument();
    expect(localStorage.getItem("dealershipUser")).toBeNull();
  });

  it("loads dealership details and publishes an authenticated review", async () => {
    localStorage.setItem(
      "dealershipUser",
      JSON.stringify({ token: "review-token", username: "reviewer" }),
    );
    const fetchMock = vi.spyOn(globalThis, "fetch")
      .mockResolvedValueOnce(jsonResponse(dealer))
      .mockResolvedValueOnce(jsonResponse([]))
      .mockResolvedValueOnce(jsonResponse({ CarModels: [{ CarMake: "Toyota", CarModel: "Camry" }] }))
      .mockResolvedValueOnce(jsonResponse({
        id: 7,
        dealership: 1,
        reviewer: "reviewer",
        text: "A friendly team.",
        purchase: true,
        purchase_date: "2026-01-01",
        car_make: "Toyota",
        car_model: "Camry",
        car_year: 2024,
        created_at: "2026-01-01T00:00:00Z",
      }, 201))
      .mockResolvedValueOnce(jsonResponse(dealer))
      .mockResolvedValueOnce(jsonResponse([{
        id: 7,
        dealership: 1,
        reviewer: "reviewer",
        text: "A friendly team.",
        purchase: true,
        purchase_date: "2026-01-01",
        car_make: "Toyota",
        car_model: "Camry",
        car_year: 2024,
        created_at: "2026-01-01T00:00:00Z",
      }]))
      .mockResolvedValueOnce(jsonResponse({ CarModels: [{ CarMake: "Toyota", CarModel: "Camry" }] }))
      .mockResolvedValueOnce(jsonResponse({ sentiment: "positive", score: 1 }));
    const user = userEvent.setup();
    renderAt("/dealers/1");

    expect(await screen.findByRole("heading", { name: "Heartland Motors" })).toBeInTheDocument();
    await user.type(screen.getByLabelText("Your review"), "A friendly team.");
    await user.click(screen.getByLabelText("I purchased a vehicle from this dealership"));
    await user.type(screen.getByLabelText("Purchase date"), "2026-01-01");
    await user.selectOptions(screen.getByLabelText("Car make"), "Toyota");
    await user.selectOptions(screen.getByLabelText("Car model"), "Camry");
    await user.type(screen.getByLabelText("Car year"), "2024");
    await user.click(screen.getByRole("button", { name: "Post review" }));

    expect(await screen.findByText("Thanks — your review has been added.")).toBeInTheDocument();
    expect(await screen.findByRole("img", { name: "positive sentiment" })).toBeInTheDocument();
    expect(await screen.findByText(/Purchased 2024 Toyota Camry/)).toBeInTheDocument();
    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(8));
    expect(screen.getAllByText("A friendly team.").length).toBeGreaterThan(0);
    const submission = fetchMock.mock.calls.find(([, options]) => options?.method === "POST");
    expect(JSON.parse(submission[1].body)).toMatchObject({
      purchase: true,
      purchase_date: "2026-01-01",
      car_make: "Toyota",
      car_model: "Camry",
      car_year: 2024,
    });
  });
});
