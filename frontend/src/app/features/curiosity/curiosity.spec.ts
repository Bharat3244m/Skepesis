import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CuriositySolver } from './curiosity-solver';

describe('CuriositySolver', () => {
  let component: CuriositySolver;
  let fixture: ComponentFixture<CuriositySolver>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CuriositySolver]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CuriositySolver);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
