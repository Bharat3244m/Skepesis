import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { provideRouter } from '@angular/router';

import { AttemptDetailsComponent } from './attempt-details.component';

describe('AttemptDetailsComponent', () => {
  let component: AttemptDetailsComponent;
  let fixture: ComponentFixture<AttemptDetailsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AttemptDetailsComponent],
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        provideRouter([])
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AttemptDetailsComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
