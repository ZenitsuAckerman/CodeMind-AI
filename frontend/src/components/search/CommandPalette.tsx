import React, { useEffect, useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Search, Folder, FileCode2, Command } from "lucide-react";
import { useAppStore } from "@/store/appStore";
import { cn } from "@/lib/utils";

const MOCK_RESULTS = [
  { id: 1, title: "Search repositories...", icon: Search, type: "action" },
  { id: 2, title: "backend/api/routes.py", icon: FileCode2, type: "file" },
  { id: 3, title: "frontend/src/components", icon: Folder, type: "folder" },
];

export function CommandPalette() {
  const { isCommandPaletteOpen, setCommandPaletteOpen } = useAppStore();
  const [search, setSearch] = useState("");
  const [selectedIndex, setSelectedIndex] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        setCommandPaletteOpen(!isCommandPaletteOpen);
      }
      if (e.key === "Escape" && isCommandPaletteOpen) {
        setCommandPaletteOpen(false);
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isCommandPaletteOpen, setCommandPaletteOpen]);

  useEffect(() => {
    if (isCommandPaletteOpen) {
      setSearch("");
      setSelectedIndex(0);
      setTimeout(() => inputRef.current?.focus(), 50);
    }
  }, [isCommandPaletteOpen]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setSelectedIndex((prev) => (prev + 1) % MOCK_RESULTS.length);
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setSelectedIndex((prev) => (prev - 1 + MOCK_RESULTS.length) % MOCK_RESULTS.length);
    } else if (e.key === "Enter") {
      e.preventDefault();
      setCommandPaletteOpen(false);
    }
  };

  return (
    <AnimatePresence>
      {isCommandPaletteOpen && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.15 }}
            className="fixed inset-0 z-50 bg-background/50 backdrop-blur-sm"
            onClick={() => setCommandPaletteOpen(false)}
          />
          <div className="fixed inset-0 z-50 flex items-start justify-center pt-[15vh] pointer-events-none">
            <motion.div
              initial={{ opacity: 0, y: -10, scale: 0.98 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -10, scale: 0.98 }}
              transition={{ duration: 0.16, ease: "easeOut" }}
              className="w-full max-w-2xl bg-background rounded-xl border border-border shadow-2xl overflow-hidden pointer-events-auto"
            >
              <div className="flex items-center border-b border-border px-4 py-3 gap-3">
                <Search className="size-5 text-muted-foreground" />
                <input
                  ref={inputRef}
                  type="text"
                  placeholder="Ask CodeMind or search files..."
                  className="flex-1 bg-transparent border-none outline-none text-base placeholder:text-muted-foreground"
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  onKeyDown={handleKeyDown}
                />
                <div className="flex items-center gap-1 text-xs text-muted-foreground font-mono bg-muted px-1.5 py-0.5 rounded">
                  <Command className="size-3" />K
                </div>
              </div>
              <div className="max-h-[60vh] overflow-y-auto p-2">
                {MOCK_RESULTS.map((result, index) => {
                  const Icon = result.icon;
                  const isSelected = index === selectedIndex;
                  return (
                    <div
                      key={result.id}
                      className={cn(
                        "flex items-center gap-3 px-3 py-2.5 rounded-md cursor-pointer transition-colors text-sm",
                        isSelected ? "bg-muted text-foreground" : "text-muted-foreground hover:bg-muted/50 hover:text-foreground"
                      )}
                      onMouseEnter={() => setSelectedIndex(index)}
                      onClick={() => setCommandPaletteOpen(false)}
                    >
                      <Icon className="size-4" />
                      {result.title}
                    </div>
                  );
                })}
              </div>
            </motion.div>
          </div>
        </>
      )}
    </AnimatePresence>
  );
}
