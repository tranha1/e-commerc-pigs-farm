import { useQuery } from '@tanstack/react-query';
import { apiService, Pig, Medicine } from '@/services/api';

export const usePigDetail = (pigId: number | undefined) => {
  return useQuery({
    queryKey: ['pig', pigId],
    queryFn: () => apiService.getPig(pigId!),
    enabled: !!pigId,
    staleTime: 5 * 60 * 1000, // 5 minutes
    gcTime: 10 * 60 * 1000, // 10 minutes
  });
};

export const useMedicineDetail = (medicineId: number | undefined) => {
  return useQuery({
    queryKey: ['medicine', medicineId],
    queryFn: () => apiService.getMedicine(medicineId!),
    enabled: !!medicineId,
    staleTime: 5 * 60 * 1000, // 5 minutes
    gcTime: 10 * 60 * 1000, // 10 minutes
  });
};

// Hook để lấy chi tiết sản phẩm chung (pig hoặc medicine)
export const useProductDetail = (type: 'pig' | 'medicine', id: number | undefined) => {
  const pigQuery = usePigDetail(type === 'pig' ? id : undefined);
  const medicineQuery = useMedicineDetail(type === 'medicine' ? id : undefined);
  
  if (type === 'pig') {
    return {
      product: pigQuery.data?.data,
      loading: pigQuery.isLoading,
      error: pigQuery.error,
      type: 'pig' as const
    };
  } else {
    return {
      product: medicineQuery.data?.data,
      loading: medicineQuery.isLoading,
      error: medicineQuery.error,
      type: 'medicine' as const
    };
  }
};