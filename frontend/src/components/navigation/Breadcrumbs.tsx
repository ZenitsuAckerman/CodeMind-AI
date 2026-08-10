import React from "react";
import { ChevronRight } from "lucide-react";
import { useLocation } from "react-router-dom";
import { cn } from "@/lib/utils";

export function Breadcrumbs() {
  const location = useLocation();
  const paths = location.pathname.split("/").filter(Boolean);

  if (paths.length === 0) return null;

  return (
    <div className="flex items-center gap-1 text-sm font-medium text-muted-foreground">
      <span className="hover:text-foreground cursor-pointer transition-colors">Home</span>
      {paths.map((path, index) => (
        <React.Fragment key={path}>
          <ChevronRight className="size-4" />
          <span 
            className={cn(
              "capitalize", 
              index === paths.length - 1 ? "text-foreground" : "hover:text-foreground cursor-pointer transition-colors"
            )}
          >
            {path}
          </span>
        </React.Fragment>
      ))}
    </div>
  );
}
