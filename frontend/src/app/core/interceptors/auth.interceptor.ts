import { HttpInterceptorFn } from '@angular/common/http';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const isApiRequest = req.url.includes('localhost:8000');

  if (isApiRequest) {
    const clonedReq = req.clone({
      withCredentials: true
    });
    return next(clonedReq);
  }

  return next(req);
};
