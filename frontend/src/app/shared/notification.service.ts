import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class NotificationService {
  private notifier = new Subject<{ message: string; type: string }>();
  notifications$ = this.notifier.asObservable();

  show(message: string, type: 'info' | 'success' | 'error' = 'info') {
    this.notifier.next({ message, type });
  }
}
