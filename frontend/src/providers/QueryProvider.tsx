import React from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // Data considered fresh for 5 minutes
      gcTime: 1000 * 60 * 15,   // Garbage collect unused data after 15 minutes
      refetchOnWindowFocus: "always", // Ensure data is fresh when returning to the tab
      retry: (failureCount, error: any) => {
        // Don't retry on 401/403/404 errors
        const status = error?.response?.status;
        if (status === 401 || status === 403 || status === 404) return false;
        return failureCount < 3; // Retry up to 3 times for transient errors
      },
      retryDelay: attemptIndex => Math.min(1000 * 2 ** attemptIndex, 30000), // Exponential backoff
    },
  },
});

export function QueryProvider({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
}
