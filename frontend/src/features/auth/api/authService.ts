import { api } from "@/lib/api";
import { z } from "zod";

export const loginSchema = z.object({
  email: z.string().email("Please enter a valid email address."),
  password: z.string().min(1, "Password is required."),
});

export const registerSchema = z.object({
  email: z.string().email("Please enter a valid email address."),
  full_name: z.string().min(2, "Full name must be at least 2 characters.").optional(),
  password: z.string().min(8, "Password must be at least 8 characters."),
});

export type LoginCredentials = z.infer<typeof loginSchema>;
export type RegisterCredentials = z.infer<typeof registerSchema>;

export const authService = {
  login: async (data: LoginCredentials) => {
    // The backend uses OAuth2PasswordRequestForm which expects form-data
    const params = new URLSearchParams();
    params.append('username', data.email);
    params.append('password', data.password);
    
    const response = await api.post('/auth/login', params, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    });
    return response.data; // Expected: { access_token: string, token_type: string }
  },
  
  register: async (data: RegisterCredentials) => {
    const response = await api.post('/auth/register', data);
    return response.data;
  },
  
  me: async () => {
    const response = await api.get('/auth/me');
    return response.data;
  }
};
