import { useState, useRef, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { 
  ArrowLeft, 
  Settings, 
  Database, 
  Send, 
  Loader2, 
  FileCode2
} from "lucide-react";
import { toast } from "sonner";

import { useProject } from "../api/projectService";
import { chatApi } from "../api/chatService";
import type { Citation } from "../api/chatService";
import { LoadingState } from "@/components/feedback/LoadingState";
import { ErrorState } from "@/components/feedback/ErrorState";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { MarkdownViewer } from "@/components/ui/markdown-viewer";
import { CitationBadge } from "../components/CitationModal";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  citations?: Citation[];
  timestamp: string;
}

export function ProjectDetail() {
  const { id } = useParams<{ id: string }>();
  const { data: project, isLoading, isError, refetch } = useProject(id!);

  const [messages, setMessages] = useState<Message[]>([
    {
      id: "welcome-msg",
      role: "assistant",
      content: "Workspace RAG engine initialized. Ask a technical question about the indexed architecture or codebase logic.",
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    }
  ]);

  const [inputQuestion, setInputQuestion] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isSubmitting]);

  const handleSendMessage = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    const query = inputQuestion.trim();
    if (!query || isSubmitting || !id) return;

    const userMsg: Message = {
      id: `user-${Date.now()}`,
      role: "user",
      content: query,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputQuestion("");
    setIsSubmitting(true);

    try {
      const res = await chatApi.chatWithProject(id, query);
      const assistantMsg: Message = {
        id: `assistant-${Date.now()}`,
        role: "assistant",
        content: res.answer,
        citations: res.citations,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err: any) {
      toast.error(err.response?.data?.detail || "Failed to query repository knowledge base");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  if (isLoading) {
    return <LoadingState message="Loading project workspace..." />;
  }

  if (isError || !project) {
    return <ErrorState message="Failed to load project details." onRetry={() => refetch()} />;
  }

  return (
    <div className="flex flex-col h-[calc(100vh-6.5rem)] -m-4 md:-m-6 lg:-m-8">
      {/* Top Action Bar */}
      <div className="h-12 border-b border-border bg-background px-4 flex items-center justify-between shrink-0">
        <div className="flex items-center gap-3">
          <Button variant="ghost" size="icon" asChild className="h-8 w-8 text-muted-foreground hover:text-foreground">
            <Link to="/dashboard" title="Back to Projects">
              <ArrowLeft className="size-4" />
            </Link>
          </Button>
          <div className="h-4 w-px bg-border" />
          <div className="flex items-center gap-2 font-mono text-xs">
            <span className="text-foreground font-medium">{project.name}</span>
            <span className="text-muted-foreground">/</span>
            <span className="text-muted-foreground truncate max-w-xs">{project.description || "main"}</span>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1.5 px-2 py-0.5 rounded text-[11px] font-mono bg-emerald-500/10 text-emerald-500 border border-emerald-500/20">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
            Vector Store Ready
          </div>
          <Button variant="outline" size="sm" className="h-8 text-xs gap-1.5">
            <Settings className="size-3.5" />
            Settings
          </Button>
        </div>
      </div>

      {/* Main Workspace Split Pane */}
      <div className="flex-1 flex min-h-0 bg-background">
        {/* Left/Main Knowledge Engine Chat Pane */}
        <div className="flex-1 flex flex-col min-w-0 border-r border-border">
          {/* Conversation Thread */}
          <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-6">
            {messages.map((msg) => (
              <div
                key={msg.id}
                className="flex flex-col gap-1.5 max-w-3xl"
              >
                <div className="flex items-center gap-2 text-xs font-mono text-muted-foreground">
                  <span className="font-semibold text-foreground">
                    {msg.role === "user" ? "You" : "CodeMind Engine"}
                  </span>
                  <span>•</span>
                  <span>{msg.timestamp}</span>
                </div>

                <div className={`p-4 rounded-xl border text-sm leading-relaxed ${
                  msg.role === "user" 
                    ? "bg-muted/40 border-border text-foreground" 
                    : "bg-background border-border shadow-sm text-foreground"
                }`}>
                  <MarkdownViewer content={msg.content} />

                  {/* Citations section */}
                  {msg.citations && msg.citations.length > 0 && (
                    <div className="mt-4 pt-3 border-t border-border/60">
                      <div className="text-[11px] font-mono text-muted-foreground mb-1.5 flex items-center gap-1">
                        <FileCode2 className="size-3" />
                        Retrieved Citations:
                      </div>
                      <div className="flex flex-wrap gap-1">
                        {msg.citations.map((cite, idx) => (
                          <CitationBadge key={`${cite.document_id}-${idx}`} citation={cite} index={idx} />
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ))}

            {isSubmitting && (
              <div className="flex flex-col gap-1.5 max-w-3xl">
                <div className="flex items-center gap-2 text-xs font-mono text-muted-foreground">
                  <span className="font-semibold text-foreground">CodeMind Engine</span>
                  <span>•</span>
                  <span className="animate-pulse">Thinking...</span>
                </div>
                <div className="p-4 rounded-xl border border-border bg-background shadow-sm flex items-center gap-3">
                  <Loader2 className="size-4 animate-spin text-blue-accent" />
                  <span className="text-xs font-mono text-muted-foreground">Retrieving vector chunks and executing model inference...</span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Prompt Input Form */}
          <div className="p-4 border-t border-border bg-background shrink-0">
            <form onSubmit={handleSendMessage} className="relative flex items-center">
              <Textarea
                ref={textareaRef}
                value={inputQuestion}
                onChange={(e) => setInputQuestion(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask about repository architecture, functions, or execution flows... (Enter to send, Shift+Enter for newline)"
                className="pr-12 min-h-[52px] max-h-36 resize-none font-mono text-xs bg-muted/20 border-border focus-visible:ring-1 focus-visible:ring-blue-accent"
                disabled={isSubmitting}
              />
              <Button
                type="submit"
                size="icon"
                variant="primary"
                disabled={!inputQuestion.trim() || isSubmitting}
                className="absolute right-2 top-2.5 h-7 w-7 rounded-md"
              >
                {isSubmitting ? <Loader2 className="size-3.5 animate-spin" /> : <Send className="size-3.5" />}
              </Button>
            </form>
          </div>
        </div>

        {/* Right Repository & Document Inspector Panel */}
        <div className="w-80 hidden lg:flex flex-col border-l border-border bg-muted/10 shrink-0">
          <div className="h-10 px-4 border-b border-border flex items-center justify-between bg-background">
            <span className="text-xs font-mono font-medium text-foreground flex items-center gap-1.5">
              <Database className="size-3.5 text-blue-accent" />
              Repository Index
            </span>
            <span className="text-[10px] font-mono bg-muted px-1.5 py-0.5 rounded text-muted-foreground">Qdrant Active</span>
          </div>

          <div className="p-4 flex flex-col gap-4 overflow-y-auto">
            <div className="rounded-lg border border-border bg-background p-3">
              <div className="text-xs font-semibold text-foreground mb-1">Index Metadata</div>
              <div className="space-y-1 text-[11px] font-mono text-muted-foreground">
                <div className="flex justify-between"><span>Embedding:</span> <span className="text-foreground">Text-Embedding-3</span></div>
                <div className="flex justify-between"><span>Chunk Size:</span> <span className="text-foreground">512 tokens</span></div>
                <div className="flex justify-between"><span>Distance Metric:</span> <span className="text-foreground">Cosine</span></div>
              </div>
            </div>

            <div className="flex flex-col gap-2">
              <div className="text-xs font-mono text-muted-foreground font-medium uppercase tracking-wider">Indexed Documents</div>
              <div className="space-y-1.5">
                {[
                  { name: "backend/app/api/v1/endpoints/projects.py", status: "Indexed" },
                  { name: "backend/app/services/chat_service.py", status: "Indexed" },
                  { name: "frontend/src/App.tsx", status: "Indexed" },
                  { name: "frontend/src/store/appStore.ts", status: "Indexed" },
                ].map((doc, idx) => (
                  <div key={idx} className="flex items-center justify-between p-2 rounded border border-border/60 bg-background text-xs font-mono">
                    <div className="flex items-center gap-2 truncate">
                      <FileCode2 className="size-3.5 text-muted-foreground shrink-0" />
                      <span className="truncate text-foreground" title={doc.name}>{doc.name}</span>
                    </div>
                    <span className="text-[10px] text-emerald-500 font-medium shrink-0">{doc.status}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
