import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GammaExposureComponent } from './gamma-exposure.component';

describe('GammaExposureComponent', () => {
  let component: GammaExposureComponent;
  let fixture: ComponentFixture<GammaExposureComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GammaExposureComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(GammaExposureComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
