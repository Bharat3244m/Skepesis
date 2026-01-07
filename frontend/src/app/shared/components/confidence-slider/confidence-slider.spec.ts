import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ConfidenceSlider } from './confidence-slider';

describe('ConfidenceSlider', () => {
  let component: ConfidenceSlider;
  let fixture: ComponentFixture<ConfidenceSlider>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ConfidenceSlider]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ConfidenceSlider);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
