import { useQuery } from '@tanstack/react-query';
import { apiService, ApiParams, Medicine, Pig } from '@/services/api';

export const useMedicines = (params?: ApiParams) => {
  return useQuery({
    queryKey: ['medicines', params],
    queryFn: () => apiService.getMedicines(params),
    staleTime: 5 * 60 * 1000, // 5 minutes
    gcTime: 10 * 60 * 1000, // 10 minutes (was cacheTime)
  });
};

export const usePigs = (params?: ApiParams) => {
  return useQuery({
    queryKey: ['pigs', params],
    queryFn: () => apiService.getPigs(params),
    staleTime: 5 * 60 * 1000,
    gcTime: 10 * 60 * 1000,
  });
};

export const useHealthCheck = () => {
  return useQuery({
    queryKey: ['health'],
    queryFn: () => apiService.healthCheck(),
    staleTime: 30 * 1000, // 30 seconds
  });
};