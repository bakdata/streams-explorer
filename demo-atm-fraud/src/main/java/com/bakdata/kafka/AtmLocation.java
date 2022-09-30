package com.bakdata.kafka;

import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
public class AtmLocation {
    public AtmLocation(final String atmLabel, final double longitude, final double latitude) {
        this.atmLabel = atmLabel;
        this.longitude = longitude;
        this.latitude = latitude;
    }

    private String atmLabel;
    private double longitude;
    private double latitude;
}
