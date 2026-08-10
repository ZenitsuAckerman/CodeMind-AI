
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeHighlight from "rehype-highlight";
import "highlight.js/styles/github-dark.css";
import { cn } from "@/lib/utils";

interface MarkdownViewerProps {
  content: string;
  className?: string;
}

export function MarkdownViewer({ content, className }: MarkdownViewerProps) {
  return (
    <div
      className={cn(
        "prose prose-neutral dark:prose-invert max-w-none text-sm leading-relaxed",
        "prose-pre:bg-muted/80 prose-pre:border prose-pre:border-border prose-pre:rounded-lg prose-pre:p-3",
        "prose-code:font-mono prose-code:text-xs prose-code:bg-muted prose-code:px-1.5 prose-code:py-0.5 prose-code:rounded prose-code:before:content-none prose-code:after:content-none",
        "prose-p:my-2 prose-headings:font-semibold prose-headings:tracking-tight prose-ul:my-2 prose-ol:my-2",
        className
      )}
    >
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeHighlight]}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}
