// FAUST Syntax Highlighting Test File
import("stdfaust.lib");

declare name "SynthTest";
declare author "Test";

// Comments should be gray/green
/* Block comment test */

// Numbers should be purple: 440, 0.5, 1.0, 48000
freq = 440;
amp = 0.5;

// Strings only in declare/UI - NOT variable assignment
declare title "My Synth";

// Library prefixes: os. fi. de. en. no. ma.
osc1 = os.osc(freq);
lpf = fi.lowpass(2, 2000);      // Filter function (apply to signal)
dly = de.delay(48000, 1000);    // Delay function (apply to signal)
env = en.adsr(0.01, 0.1, 0.8, 0.2, 1);  // ADSR with gate=1

// Operators: =, +, -, *, /, <:, :>
mix = osc1 * amp;

// Signal chain: osc -> filter -> output * envelope
process = mix : lpf * env;