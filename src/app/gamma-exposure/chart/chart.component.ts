import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';

import { ChartSettings } from '../chart-settings.model';
import { ChartSettingsService } from '../chart.service';

@Component({
    selector: 'app-chart',
    templateUrl: './chart.component.html',
    styleUrls: ['./chart.component.css'],
})
export class ChartComponent implements OnInit, OnDestroy {
    chartSettings: ChartSettings;
    private chartSettingsSub: Subscription;

    constructor(public chartSettingsService: ChartSettingsService) {}


    ngOnInit() {
        this.chartSettingsService.getSettings();
        this.chartSettingsSub = this.chartSettingsService.getSettingsUpdateListener()
        .subscribe((chartSettings: ChartSettings) => {
            this.chartSettings = chartSettings;
        });

    }

    ngOnDestroy() {
        //prevent memory leaks
        this.chartSettingsSub.unsubscribe();
    }
}
