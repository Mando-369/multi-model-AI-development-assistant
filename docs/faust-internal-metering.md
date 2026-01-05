---
name: faust-internal-metering
description: How to add RMS/Peak metering at any point in a Faust DSP for debugging with MCP
---

## Faust MCP Internal Metering

By default, the Faust MCP automatically adds RMS/Peak meters on the DSP **outputs**. But you can also add measurement points **anywhere** in the signal graph to debug intermediate stages.

## Metering Functions

Add these definitions to your Faust code:

```faust
import("stdfaust.lib");

// RMS meter (linear)
mcp_rms(x) = x <: attach(_, an.rms_envelope_rect(0.1) : hbargraph("RMS", 0, 1));

// Peak meter (linear)
mcp_peak(x) = x <: attach(_, an.peak_envelope(0.1) : hbargraph("Peak", 0, 1));

// Full meter (RMS + Peak)
mcp_meter = mcp_rms : mcp_peak;
```

## Usage

### Measuring an intermediate signal

```faust
// Measure after oscillator, before filter
osc = os.sawtooth(freq) : mcp_meter;
filtered = osc : fi.lowpass(2, cutoff);
process = filtered;
```

### Measuring with a custom label

```faust
mcp_rms_named(name, x) = x <: attach(_, an.rms_envelope_rect(0.1) : hbargraph("%name RMS", 0, 1));
mcp_peak_named(name, x) = x <: attach(_, an.peak_envelope(0.1) : hbargraph("%name Peak", 0, 1));
mcp_meter_named(name) = mcp_rms_named(name) : mcp_peak_named(name);

// Usage
osc = os.sawtooth(freq) : mcp_meter_named("Osc");
env = en.adsr(0.01, 0.1, 0.7, 0.3, gate) : mcp_meter_named("Env");
```

### Measuring multiple points

```faust
import("stdfaust.lib");

mcp_meter(name, x) = x <: attach(_, an.rms_envelope_rect(0.1) : hbargraph("h:Debug/%name", 0, 1));

freq = hslider("freq", 440, 20, 2000, 1);
gain = hslider("gain", 0.5, 0, 1, 0.01);
gate = button("gate");

// Pipeline with metering at each stage
osc = os.sawtooth(freq) : mcp_meter("1-Osc");
shaped = osc * en.adsr(0.01, 0.1, 0.7, 0.3, gate) : mcp_meter("2-Env");
output = shaped * gain : mcp_meter("3-Output");

process = output <: _, _;
```

## Reading Values

The added bargraphs appear in `get_param_values()` as linear values (0-1 range):

```json
{
  "path": "/dsp/Debug/1-Osc",
  "value": 0.57
},
{
  "path": "/dsp/Debug/2-Env",
  "value": 0.42
},
{
  "path": "/dsp/Debug/3-Output",
  "value": 0.21
}
```

These values are directly comparable with `get_audio_metrics()` output.

## Use Cases

1. **Debug a disappearing signal**: Add meters at each stage to locate where the signal drops to zero or becomes NaN.

2. **Check levels before/after an effect**: Compare the gain of a filter or distortion.

3. **Monitor an envelope**: Verify that the ADSR rises and falls correctly.

4. **Detect internal clipping**: Find where the signal exceeds 1.0 before the final output.

## Notes

- `attach(x, y)` passes `x` through unchanged, but forces computation of `y` (side-effect for the bargraph)
- Meters add slight CPU overhead (0.1s RMS/Peak window)
- Use groups (`h:Debug/...`) to organize meters in the UI
- Values are linear (not dB) for easy comparison: `0.5` = half amplitude, `1.0` = full scale, `> 1.0` = clipping
