import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OptionsDataComponent } from './options-data.component';

describe('OptionsDataComponent', () => {
  let component: OptionsDataComponent;
  let fixture: ComponentFixture<OptionsDataComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ OptionsDataComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(OptionsDataComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
