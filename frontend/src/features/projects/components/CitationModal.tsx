import { useState } from "react";
import { FileCode2 } from "lucide-react";
import type { Citation } from "../api/chatService";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";

interface CitationBadgeProps {
  citation: Citation;
  index: number;
}

export function CitationBadge({ citation, index }: CitationBadgeProps) {
  const [open, setOpen] = useState(false);

  return (
    <>
      <button
        onClick={() => setOpen(true)}
        className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-mono font-medium bg-blue-accent/10 text-blue-accent border border-blue-accent/20 hover:bg-blue-accent/20 transition-colors cursor-pointer my-1 mr-1.5"
        title={`View Citation Source (Doc: ${citation.document_id})`}
      >
        <FileCode2 className="size-3" />
        <span>cite:{index + 1}</span>
      </button>

      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2 font-mono text-sm">
              <FileCode2 className="size-4 text-blue-accent" />
              Document Citation #{index + 1}
            </DialogTitle>
            <DialogDescription className="text-xs font-mono text-muted-foreground pt-1">
              Doc ID: {citation.document_id} • Chunk Index: {citation.chunk_index}
            </DialogDescription>
          </DialogHeader>

          <div className="bg-muted/60 border border-border rounded-lg p-4 font-mono text-xs overflow-x-auto my-2 max-h-60">
            <div className="text-muted-foreground select-none pb-2 border-b border-border/50 mb-2">
              // Retrieved Chunk Metadata (Vector Store ID: {citation.document_id})
            </div>
            <pre className="text-foreground leading-relaxed">
              {`// Referenced chunk #${citation.chunk_index}
// Context retrieved from indexed repository files.
// File matching ID: ${citation.document_id}`}
            </pre>
          </div>

          <div className="flex justify-end gap-2 pt-2">
            <Button variant="outline" size="sm" onClick={() => setOpen(false)}>
              Close Inspector
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </>
  );
}
