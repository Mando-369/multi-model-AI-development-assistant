---
name: faust-internal-metering
description: How to add RMS/Peak metering at any point in a Faust DSP for debugging with MCP
---

## Faust MCP Internal Metering

By default, the Faust MCP automatically adds RMS/Peak meters on the DSP **outputs**. But you can also add measurement points **anywhere** in the signal graph to debug intermediate stages.

## Probe Metering (Recommended)

Use `[probe:N]` metadata to add structured metering points that appear in `get_audio_metrics()`:

```faust
import("stdfaust.lib");

// RMS probe in dB (auto-converts to linear in get_audio_metrics)
probe_rms_db(id, hide, x) = x <: attach(x, an.rms_envelope_rect(0.1)
  : max(0.00001) : ba.linear2db
  : hbargraph("Probe RMS%2id[probe:%id][unit:dB][hidden:%hide]", -60, 0));

// RMS probe in linear (returned as-is)
probe_rms_lin(id, hide, x) = x <: attach(x, an.rms_envelope_rect(0.1)
  : hbargraph("Probe RMS%2id[probe:%id][hidden:%hide]", 0, 1));

// Peak probe in dB
probe_peak_db(id, hide, x) = x <: attach(x, an.peak_envelope(0.1)
  : max(0.00001) : ba.linear2db
  : hbargraph("Probe Peak%2id[probe:%id][unit:dB][hidden:%hide]", -60, 0));

// Peak probe in linear
probe_peak_lin(id, hide, x) = x <: attach(x, an.peak_envelope(0.1)
  : hbargraph("Probe Peak%2id[probe:%id][hidden:%hide]", 0, 1));
```

### Usage

```faust
freq = hslider("freq", 440, 20, 2000, 1);
gain = hslider("gain", 0.5, 0, 1, 0.01);
gate = button("gate");

// Pipeline with probes at each stage
osc = os.sawtooth(freq) : probe_rms_db(0, 0);
shaped = osc * en.adsr(0.01, 0.1, 0.7, 0.3, gate) : probe_rms_db(1, 0);
output = shaped * gain : probe_rms_db(2, 0);

process = output <: _,_;
```

### Reading Probe Values

Probes appear in `get_audio_metrics()` under the `probes` array:

```json
{
  "mix": { "rms": 0.23, "peak": 0.45, "hasNaN": false },
  "channels": [
    { "rms": 0.2, "peak": 0.42 },
    { "rms": 0.25, "peak": 0.48 }
  ],
  "probes": [
    { "id": 0, "value": 0.57 },
    { "id": 1, "value": 0.42 },
    { "id": 2, "value": 0.21 }
  ]
}
```

### Metadata Reference

| Metadata | Effect |
|----------|--------|
| `[probe:N]` | Adds bargraph to `probes` array with `id: N` |
| `[unit:dB]` | Auto-converts dB value to linear in `get_audio_metrics()` |
| `[hidden:1]` | Hides bargraph in compatible UIs |

## Legacy Metering (Simple)

For quick debugging without structured probe access:

```faust
import("stdfaust.lib");

// RMS meter (linear)
mcp_rms(x) = x <: attach(_, an.rms_envelope_rect(0.1) : hbargraph("RMS", 0, 1));

// Peak meter (linear)
mcp_peak(x) = x <: attach(_, an.peak_envelope(0.1) : hbargraph("Peak", 0, 1));

// Full meter (RMS + Peak)
mcp_meter = mcp_rms : mcp_peak;
```

### Measuring with a custom label

```faust
mcp_meter(name, x) = x <: attach(_, an.rms_envelope_rect(0.1) : hbargraph("h:Debug/%name", 0, 1));

// Usage
osc = os.sawtooth(freq) : mcp_meter("1-Osc");
shaped = osc * en.adsr(0.01, 0.1, 0.7, 0.3, gate) : mcp_meter("2-Env");
```

These appear in `get_param_values()` as linear values:

```json
{
  "path": "/dsp/Debug/1-Osc",
  "value": 0.57
}
```

## Use Cases

1. **Debug a disappearing signal**: Add probes at each stage to locate where the signal drops to zero or becomes NaN.

2. **Check levels before/after an effect**: Compare the gain of a filter or distortion.

3. **Monitor an envelope**: Verify that the ADSR rises and falls correctly.

4. **Detect internal clipping**: Find where the signal exceeds 1.0 before the final output.

## Notes

- `attach(x, y)` passes `x` through unchanged, but forces computation of `y` (side-effect for the bargraph)
- Meters add slight CPU overhead (0.1s RMS/Peak window)
- Probes with `[unit:dB]` are auto-converted to linear: `10^(dB/20)`
- Linear values: `0.5` = half amplitude, `1.0` = full scale, `> 1.0` = clipping
