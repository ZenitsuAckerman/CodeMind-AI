import React, { Suspense } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { ErrorBoundary } from "react-error-boundary";

// Layouts and Providers (Load eagerly as they wrap the app)
import { AppLayout } from "@/components/layout/AppLayout";
import { AuthLayout } from "@/components/layout/AuthLayout";
import { ProtectedRoute } from "@/components/layout/ProtectedRoute";
import { ThemeProvider } from "@/providers/ThemeProvider";
import { QueryProvider } from "@/providers/QueryProvider";

// Feedback Components
import { LoadingState } from "@/components/feedback/LoadingState";
import { ErrorState } from "@/components/feedback/ErrorState";

// Route-Level Code Splitting (Lazy Load Pages)
const LandingPage = React.lazy(() => import("@/routes/LandingPage").then(m => ({ default: m.LandingPage })));
const NotFound = React.lazy(() => import("@/routes/NotFound").then(m => ({ default: m.NotFound })));
const Login = React.lazy(() => import("@/features/auth/routes/Login").then(m => ({ default: m.Login })));
const Register = React.lazy(() => import("@/features/auth/routes/Register").then(m => ({ default: m.Register })));
const Dashboard = React.lazy(() => import("@/features/projects/routes/Dashboard").then(m => ({ default: m.Dashboard })));
const ProjectDetail = React.lazy(() => import("@/features/projects/routes/ProjectDetail").then(m => ({ default: m.ProjectDetail })));

function App() {
  return (
    <ErrorBoundary FallbackComponent={ErrorState} onReset={() => window.location.reload()}>
      <QueryProvider>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          <BrowserRouter>
            <Suspense fallback={<LoadingState message="Loading CodeMind..." />}>
              <Routes>
                {/* Public Routes */}
                <Route path="/" element={<LandingPage />} />
                
                {/* Auth Routes */}
                <Route element={<AuthLayout />}>
                  <Route path="/login" element={<Login />} />
                  <Route path="/register" element={<Register />} />
                </Route>

                {/* Protected Application Routes */}
                <Route element={<ProtectedRoute />}>
                  <Route element={<AppLayout />}>
                    <Route path="/dashboard" element={<Dashboard />} />
                    <Route path="/projects" element={<Dashboard />} />
                    <Route path="/projects/:id" element={<ProjectDetail />} />
                    
                    {/* 404 Catch-All inside Dashboard */}
                    <Route path="*" element={<NotFound />} />
                  </Route>
                </Route>
              </Routes>
            </Suspense>
          </BrowserRouter>
        </ThemeProvider>
      </QueryProvider>
    </ErrorBoundary>
  );
}

export default App;
