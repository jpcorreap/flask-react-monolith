import { useCallback, useMemo } from "react";

const fetch_url = "http://localhost:5000";

export default function useFetchRequest() {
  const _getHeaders = useCallback(async (token) => {
    const headers = new Headers();
    headers.append("Content-Type", "application/json");
    if (token) headers.append("Authorization", `Bearer ${token}`);
    return headers;
  }, []);

  // eslint-disable-next-line no-unused-vars
  const _handleError = useCallback((response) => {
    const errorDetail = {
      statusText: response.statusText,
      status: response.status,
      url: response.url,
    };
    if (response.status === 404) {
      console.error("404 not found", errorDetail);
    }
    if (response.status === 403 || response.status === 401) {
      console.error("403 o 401 Acceso no permitido", errorDetail);
    }
    console.error("Error genérico", errorDetail);
  }, []);

  return useMemo(
    () => ({
      async get(path, token) {
        const headers = await _getHeaders(token);
        return fetch(fetch_url + path, { headers, method: "GET" });
      },

      async patch(path, body, token) {
        const headers = await _getHeaders(token);
        return fetch(fetch_url + path, {
          headers,
          method: "PATCH",
          body: JSON.stringify(body),
        });
      },

      async post(path, body, token) {
        const headers = await _getHeaders(token);
        return fetch(fetch_url + path, {
          headers,
          method: "POST",
          body: JSON.stringify(body),
        });
      },
    }),
    [_getHeaders]
  );
}
