import { Component } from '@angular/core';
import { CommonModule } from '@angular/common'; // Required for *ngIf
import { RouterModule, Router } from '@angular/router'; // Required for routerLink
import { AuthService } from '../../services/auth';

@Component({
  standalone: true,
  selector: 'app-layout',
  templateUrl: './layout.html',
  // No separate CSS file needed if you are using the global styles.css
  imports: [CommonModule, RouterModule]
})
export class LayoutComponent {

  constructor(
    public auth: AuthService, // Public so HTML can see it
    private router: Router
  ) {}

  logout() {
    this.auth.logout();
    this.router.navigate(['/login']);
  }
}
