import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AttemptDetails } from './attempt-details';

describe('AttemptDetails', () => {
  let component: AttemptDetails;
  let fixture: ComponentFixture<AttemptDetails>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AttemptDetails]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AttemptDetails);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
