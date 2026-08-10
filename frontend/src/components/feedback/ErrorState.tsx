import { motion } from "framer-motion";
import { AlertCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface ErrorStateProps {
  message?: string;
  onRetry?: () => void;
  error?: any;
  resetErrorBoundary?: () => void;
  className?: string;
}

export function ErrorState({ message, onRetry, error, resetErrorBoundary, className }: ErrorStateProps) {
  const retryAction = resetErrorBoundary || onRetry;
  const errorMessage = error?.message || message || "An unexpected error occurred.";

  return (
    <motion.div 
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.2, ease: "easeOut" }}
      className={cn("flex flex-col items-center justify-center text-center p-8 h-full min-h-[300px]", className)}
    >
      <div className="w-12 h-12 rounded-xl bg-red-500/10 flex items-center justify-center text-red-500 mb-4">
        <AlertCircle className="size-6" />
      </div>
      <h3 className="text-lg font-semibold tracking-tight text-foreground mb-2">Something went wrong</h3>
      <p className="text-sm text-muted-foreground mb-6 max-w-sm">
        {errorMessage}
      </p>

      {retryAction && (
        <Button variant="outline" onClick={retryAction}>
          Try Again
        </Button>
      )}
    </motion.div>
  );
}
