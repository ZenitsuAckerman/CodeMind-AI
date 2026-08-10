import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { motion } from "framer-motion";
import { Loader2 } from "lucide-react";
import { toast } from "sonner";

import { authService, registerSchema, type RegisterCredentials } from "../api/authService";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export function Register() {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);

  const { register, handleSubmit, formState: { errors } } = useForm<RegisterCredentials>({
    resolver: zodResolver(registerSchema),
  });

  const onSubmit = async (data: RegisterCredentials) => {
    try {
      setIsLoading(true);
      await authService.register(data);
      
      toast.success("Account created successfully. Please sign in.");
      navigate("/login");
    } catch (error: any) {
      toast.error(error.response?.data?.detail || "An error occurred during registration");
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
        <h1 className="text-2xl font-semibold tracking-tight text-foreground">Create an Account</h1>
        <p className="text-sm text-muted-foreground">Join CodeMind to start exploring your repositories.</p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-5">
        <div className="flex flex-col gap-2">
          <Label htmlFor="full_name">Full Name</Label>
          <Input 
            id="full_name" 
            placeholder="John Doe"
            disabled={isLoading}
            {...register("full_name")}
          />
          {errors.full_name && <span className="text-xs text-red-500 font-medium">{errors.full_name.message}</span>}
        </div>
        
        <div className="flex flex-col gap-2">
          <Label htmlFor="email">Email</Label>
          <Input 
            id="email" 
            type="email" 
            placeholder="name@example.com"
            disabled={isLoading}
            {...register("email")}
          />
          {errors.email && <span className="text-xs text-red-500 font-medium">{errors.email.message}</span>}
        </div>
        
        <div className="flex flex-col gap-2">
          <Label htmlFor="password">Password</Label>
          <Input 
            id="password" 
            type="password" 
            disabled={isLoading}
            {...register("password")}
          />
          {errors.password && <span className="text-xs text-red-500 font-medium">{errors.password.message}</span>}
        </div>

        <Button type="submit" variant="primary" className="w-full mt-2" disabled={isLoading}>
          {isLoading && <Loader2 className="mr-2 size-4 animate-spin" />}
          Sign Up
        </Button>
      </form>

      <div className="mt-6 text-center text-sm text-muted-foreground">
        Already have an account?{" "}
        <Link to="/login" className="text-foreground font-medium hover:underline">
          Sign in
        </Link>
      </div>
    </motion.div>
  );
}
