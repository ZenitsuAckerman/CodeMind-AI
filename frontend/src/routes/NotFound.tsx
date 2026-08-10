import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { Home, ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";

export function NotFound() {
  return (
    <div className="min-h-screen bg-background flex flex-col items-center justify-center p-6 text-center">
      <motion.div 
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
        className="max-w-md flex flex-col items-center"
      >
        <div className="w-16 h-16 rounded-2xl bg-muted flex items-center justify-center text-muted-foreground mb-6">
          <span className="font-mono text-xl font-bold tracking-tighter">404</span>
        </div>
        
        <h1 className="text-3xl font-semibold tracking-tight text-foreground mb-2">Page not found</h1>
        <p className="text-muted-foreground mb-8">
          The page you are looking for doesn't exist, has been moved, or you don't have permission to access it.
        </p>

        <div className="flex items-center gap-3">
          <Button variant="outline" asChild className="gap-2">
            <button onClick={() => window.history.back()}>
              <ArrowLeft className="size-4" />
              Go Back
            </button>
          </Button>
          <Button variant="primary" asChild className="gap-2">
            <Link to="/dashboard">
              <Home className="size-4" />
              Dashboard
            </Link>
          </Button>
        </div>
      </motion.div>
    </div>
  );
}
