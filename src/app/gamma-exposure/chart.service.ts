import { Injectable } from '@angular/core'
import { Subject } from 'rxjs';

import { ChartSettings } from './chart-settings.model';


@Injectable({providedIn: 'root'})

export class ChartSettingsService{
  private chartSettings: ChartSettings;
  private settingsUpdated = new Subject<ChartSettings>();

  getSettings(){
    return {...this.chartSettings};
  }

  getSettingsUpdateListener(){
    return this.settingsUpdated.asObservable();
  }

  addChart(ticker: string, timePeriod: number){
    const chartSettings: ChartSettings = {ticker: ticker, timePeriod: timePeriod};
    this.chartSettings = chartSettings;
    this.settingsUpdated.next({...this.chartSettings});
  }
}
