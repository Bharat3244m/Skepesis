import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet],
  template: `
    <div style="background: #222; color: #0f0; padding: 5px; text-align: center; font-size: 12px;">
      System Status: Angular is running...
    </div>

    <router-outlet></router-outlet>
  `
})
export class AppComponent {}
