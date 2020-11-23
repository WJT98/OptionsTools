import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';

import { ChartSettings } from '../chart-settings.model';
import { ChartSettingsService } from '../chart.service';
import { OptionsApiService } from '../options-api.service';
import { Options } from '../options.model';

@Component({
    selector: 'app-chart',
    templateUrl: './chart.component.html',
    styleUrls: ['./chart.component.css'],
})
export class ChartComponent implements OnInit, OnDestroy {
    chartSettings: ChartSettings;
    private chartSettingsSub: Subscription;
	private optionsSub: Subscription;
	optionsData: Options[];

	constructor(public chartSettingsService: ChartSettingsService, 
		private optionsApiService: OptionsApiService) {}


    ngOnInit() {
        this.chartSettingsService.getSettings();
        this.chartSettingsSub = this.chartSettingsService.getSettingsUpdateListener()
        .subscribe((chartSettings: ChartSettings) => {
            this.chartSettings = chartSettings;
		});
		
		this.optionsSub = this.optionsApiService
			.getOptions()
			.subscribe((optionsData: Options[]) => {
				this.optionsData = optionsData;
			}
			);

    }

    ngOnDestroy() {
        //prevent memory leaks
		this.chartSettingsSub.unsubscribe();
		this.optionsSub.unsubscribe();
    }
}
