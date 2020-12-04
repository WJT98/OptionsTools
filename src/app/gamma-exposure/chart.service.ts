import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { ChartSettings } from './chart-settings.model';


@Injectable({ providedIn: 'root' })
export class ChartSettingsService {
    private chartSettings: ChartSettings;
    private settingsUpdated = new Subject<ChartSettings>();
	constructor(private http:HttpClient){}

    getSettings() {
        this.http.get<{message:string, chartSettings:ChartSettings}>('http://localhost:3000/api/data')
        .subscribe((chartSettingsData) => {
            this.chartSettings= chartSettingsData.chartSettings;
            //Informs observers that chartSettings is updated
            this.settingsUpdated.next({ ...this.chartSettings });
        });
    }

    getSettingsUpdateListener() {
        return this.settingsUpdated.asObservable();
    }

    addChart(ticker: string, timePeriod: number) {
        const chartSettings: ChartSettings = {
            ticker: ticker,
            timePeriod: timePeriod,
		};
		/*
		this.http
		.post<{ message:string }> ('http://localhost:3000/api/data', chartSettings)
		.subscribe(responseData =>{
			console.log(responseData.message);
			this.chartSettings = chartSettings;
			this.settingsUpdated.next({ ...this.chartSettings });
		});
		*/
    }
}
