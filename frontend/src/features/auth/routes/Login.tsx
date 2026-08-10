import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { motion } from "framer-motion";
import { Loader2 } from "lucide-react";
import { toast } from "sonner";

import { useAuthStore } from "@/store/authStore";
import { authService, loginSchema, type LoginCredentials } from "../api/authService";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export function Login() {
  const navigate = useNavigate();
  const { setAuth } = useAuthStore();
  const [isLoading, setIsLoading] = useState(false);

  const { register, handleSubmit, formState: { errors } } = useForm<LoginCredentials>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (data: LoginCredentials) => {
    try {
      setIsLoading(true);
      const res = await authService.login(data);
      
      // Temporarily mock user data until /me is fully utilized
      setAuth(res.access_token, {
        id: "mock-id",
        email: data.email,
        is_active: true,
        is_superuser: false,
      });
      
      toast.success("Successfully logged in");
      navigate("/dashboard");
    } catch (error: any) {
      toast.error(error.response?.data?.detail || "Invalid email or password");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.2, ease: "easeOut" }}
      className="bg-background border border-border rounded-xl p-8 shadow-sm"
    >
      <div className="flex flex-col gap-2 mb-8 text-center">
        <h1 className="text-2xl font-semibold tracking-tight text-foreground">Sign In</h1>
        <p className="text-sm text-muted-foreground">Enter your credentials to access your workspace.</p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-5">
        <div className="flex flex-col gap-2">
          <Label htmlFor="email">Email</Label>
          <Input 
            id="email" 
            type="email" 
            placeholder="name@example.com"
            autoComplete="email"
            disabled={isLoading}
            {...register("email")}
          />
          {errors.email && <span className="text-xs text-red-500 font-medium">{errors.email.message}</span>}
        </div>
        
        <div className="flex flex-col gap-2">
          <div className="flex items-center justify-between">
            <Label htmlFor="password">Password</Label>
            <Link to="#" className="text-xs text-muted-foreground hover:text-foreground transition-colors">
              Forgot password?
            </Link>
          </div>
          <Input 
            id="password" 
            type="password" 
            autoComplete="current-password"
            disabled={isLoading}
            {...register("password")}
          />
          {errors.password && <span className="text-xs text-red-500 font-medium">{errors.password.message}</span>}
        </div>

        <Button type="submit" variant="primary" className="w-full mt-2" disabled={isLoading}>
          {isLoading && <Loader2 className="mr-2 size-4 animate-spin" />}
          Sign In
        </Button>
      </form>

      <div className="mt-6 text-center text-sm text-muted-foreground">
        Don't have an account?{" "}
        <Link to="/register" className="text-foreground font-medium hover:underline">
          Sign up
        </Link>
      </div>
    </motion.div>
  );
}
