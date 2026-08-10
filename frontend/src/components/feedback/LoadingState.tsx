import { motion } from "framer-motion";
import { Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";

interface LoadingStateProps {
  message?: string;
  className?: string;
}

export function LoadingState({ message = "Loading...", className }: LoadingStateProps) {
  return (
    <div className={cn("flex flex-col items-center justify-center p-8 h-full min-h-[300px]", className)}>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.2, ease: "easeOut", delay: 0.1 }}
        className="flex flex-col items-center gap-3"
      >
        <Loader2 className="size-5 text-muted-foreground animate-spin" />
        {message && <p className="text-sm text-muted-foreground">{message}</p>}
      </motion.div>
    </div>
  );
}
