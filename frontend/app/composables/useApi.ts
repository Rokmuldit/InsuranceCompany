export const useApi = () => {
  const config = useRuntimeConfig();
  const apiBase = config.public.apiBase;

  const fetchApi = async <T>(url: string, options: any = {}) => {
    return await $fetch<T>(url, {
      baseURL: apiBase,
      ...options,
    });
  };

  return {
    fetchApi,
  };
};
