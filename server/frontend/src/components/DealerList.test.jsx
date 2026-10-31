import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { beforeEach, describe, expect, it, vi } from "vitest";

import DealerList from "./DealerList.jsx";

describe("DealerList", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it("loads dealerships and filters the list by state", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch")
      .mockResolvedValueOnce(new Response(JSON.stringify([
        { id: 1, name: "Heartland Motors", city: "Wichita", state: "KS", description: "Local cars" },
        { id: 2, name: "Lakeside Automotive", city: "Chicago", state: "IL", description: "City cars" },
      ]), { status: 200, headers: { "Content-Type": "application/json" } }))
      .mockResolvedValueOnce(new Response(JSON.stringify([
        { id: 1, name: "Heartland Motors", city: "Wichita", state: "KS", description: "Local cars" },
      ]), { status: 200, headers: { "Content-Type": "application/json" } }));

    render(<MemoryRouter><DealerList /></MemoryRouter>);
    expect(await screen.findByText("Heartland Motors")).toBeInTheDocument();
    expect(screen.getByText("Lakeside Automotive")).toBeInTheDocument();
    fireEvent.change(screen.getByLabelText("Filter by state"), { target: { value: "KS" } });
    await waitFor(() => expect(fetchMock).toHaveBeenLastCalledWith(
      expect.stringContaining("/getdealersbystate/KS/"),
      expect.any(Object),
    ));
    expect(await screen.findByText("Heartland Motors")).toBeInTheDocument();
    await waitFor(() => expect(screen.queryByText("Lakeside Automotive")).not.toBeInTheDocument());
  });
});
