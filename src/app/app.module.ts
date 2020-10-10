//Components
import { AppComponent } from './app.component';
import { HeaderComponent } from './header/header.component';
import { GammaExposureComponent } from './gamma-exposure/gamma-exposure.component';
import { SidebarComponent } from './sidebar/sidebar.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { ChartSettingsComponent } from './gamma-exposure/chart-settings/chart-settings.component';

//Modules
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { NgModule } from '@angular/core';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatToolbarModule } from '@angular/material/toolbar';
import { FlexLayoutModule } from '@angular/flex-layout';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatDividerModule } from '@angular/material/divider';
import { MatListModule } from '@angular/material/list';
import { MatRippleModule } from '@angular/material/core';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { ChartComponent } from './gamma-exposure/chart/chart.component'
import { FormsModule } from '@angular/forms'
import { HttpClientModule } from '@angular/common/http'




@NgModule({
    declarations: [
        AppComponent,
        HeaderComponent,
        GammaExposureComponent,
        SidebarComponent,
        DashboardComponent,
        ChartSettingsComponent,
        ChartComponent,
    ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        FlexLayoutModule,
        BrowserAnimationsModule,
        MatFormFieldModule,
        MatSelectModule,
        MatToolbarModule,
        MatInputModule,
        MatIconModule,
        MatSidenavModule,
        MatDividerModule,
        MatListModule,
        MatRippleModule,
        MatButtonModule,
        MatCardModule,
        FormsModule,
        HttpClientModule
    ],
    providers: [],
    bootstrap: [AppComponent],
})
export class AppModule {}
