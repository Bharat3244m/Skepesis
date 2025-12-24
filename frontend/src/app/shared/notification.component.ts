import { Component } from '@angular/core';
import { NgFor } from '@angular/common';
import { NotificationService } from './notification.service';

@Component({
  standalone: true,
  selector: 'app-notifications',
  template: `
    <div
      *ngFor="let n of notifications"
      class="notification"
      [class]="'notification-' + n.type">
      {{ n.message }}
    </div>
  `,
  imports: [NgFor]
})
export class NotificationComponent {
  notifications: any[] = [];

  constructor(private notify: NotificationService) {
    this.notify.notifications$.subscribe(n => {
      this.notifications.push(n);
      setTimeout(() => this.notifications.shift(), 3000);
    });
  }
}
