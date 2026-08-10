
import { Outlet, Navigate } from "react-router-dom";
import { useAuthStore } from "@/store/authStore";

export function AuthLayout() {
  const { isAuthenticated } = useAuthStore();

  // If already logged in, don't show the auth pages, redirect to dashboard
  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  return (
    <div className="min-h-screen bg-background flex flex-col items-center justify-center p-6 selection:bg-blue-accent/20 selection:text-blue-accent font-sans">
      <div className="w-full max-w-sm">
        <div className="flex items-center justify-center gap-2 font-mono font-semibold tracking-tight text-xl mb-12">
          <div className="w-8 h-8 rounded bg-foreground text-background flex items-center justify-center text-sm">C</div>
          CodeMind
        </div>
        <main className="w-full">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
