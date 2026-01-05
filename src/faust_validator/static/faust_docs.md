# FAUST Libraries Documentation

Complete reference for all FAUST standard library functions.
Use this for understanding function behavior, examples, and best practices.

---

# aanl.lib
**Prefix:** `aa`

################################ aanl.lib ##########################################
A library for antialiased nonlinearities. Its official prefix is `aa`.

This library provides aliasing-suppressed nonlinearities through first-order
and second-order approximations of continuous-time signals, functions,
and convolution based on antiderivatives. This technique is particularly
effective if combined with low-factor oversampling, for example, operating
at 96 kHz or 192 kHz sample-rate.

The library contains trigonometric functions as well as other nonlinear
functions such as bounded and unbounded saturators.

Due to their limited domains or ranges, some of these functions may not
suitable for audio nonlinear processing or waveshaping, although
they have been included for completeness. Some other functions,
for example, tan() and tanh(), are only available with first-order
antialiasing due to the complexity of the antiderivative of the
x * f(x) term, particularly because of the necessity of the dilogarithm
function, which requires special implementation.

Future improvements to this library may include an adaptive
mechanism to set the ill-conditioned cases threshold to improve
performance in varying cases.

Note that the antialiasing functions introduce a delay in the path,
respectively half and one-sample delay for first and second-order functions.

Also note that due to division by differences, it is vital to use
double-precision or more to reduce errors.

The environment identifier for this library is `aa`. After importing
the standard libraries in Faust, the functions below can be called as `aa.function_name`.

#### References

* <https://github.com/grame-cncm/faustlibraries/blob/master/aanl.lib>
* Reducing the Aliasing in Nonlinear Waveshaping Using Continuous-time Convolution, Julian Parker, Vadim Zavalishin, Efflam Le Bivic, DAFX, 2016
* <http://dafx16.vutbr.cz/dafxpapers/20-DAFx-16_paper_41-PN.pdf>
########################################################################################

## aa.clip

-------`(aa.)clip`-----------
Clipping function.

---

## aa.Rsqrt

-------`(aa.)Rsqrt`----------
Real-valued sqrt().

---

## aa.Rlog

-------`(aa.)Rlog`-----------
Real-valued log().

---

## aa.Rtan

-------`(aa.)Rtan`-----------
Real-valued tan().

---

## aa.Racos

-------`(aa.)Racos`----------
Real-valued acos().

---

## aa.Rasin

-------`(aa.)Rasin`----------
Real-valued asin().

---

## aa.Racosh

-------`(aa.)Racosh`----------
Real-valued acosh()

---

## aa.Rcosh

-------`(aa.)Rcosh`----------
Real-valued cosh().

---

## aa.Rsinh

-------`(aa.)Rsinh`-----------
Real-valued sinh().

---

## aa.Ratanh

-------`(aa.)Ratanh`----------
Real-valued atanh().

---

## aa.ADAA1

-------`(aa.)ADAA1`---------------------
Generalised first-order Antiderivative Anti-Aliasing (ADAA) function.
Implements a first-order ADAA approximation to reduce aliasing
in nonlinear audio processing.
#### Usage
```faust
_ : ADAA1(EPS, f, F1) : _
```
Where:
* `EPS`: a threshold for switching between safe and ill-conditioned paths
* `f`: a function that we want to process with ADAA
* `F1`: f's first antiderivative
#### Test
```faust
aa = library("aanl.lib");
ba = library("basics.lib");
ma = library("maths.lib");
os = library("oscillators.lib");
ADAA1_test = aa.ADAA1(0.001, f, F1, os.osc(110))
with {
f(x) = aa.clip(-1.0, 1.0, x);
F1(x) = ba.if((x <= 1.0) & (x >= -1.0), 0.5 * x^2, x * ma.signum(x) - 0.5);
};
```

---

## aa.ADAA2

-------`(aa.)ADAA2`---------------------
Generalised second-order Antiderivative Anti-Aliasing (ADAA) function.
Implements a second-order ADAA approximation for even better aliasing reduction
at the cost of additional computation.
#### Usage
```faust
_ : ADAA2(EPS, f, F1, F2) : _
```
Where:
* `EPS`: a threshold for switching between safe and ill-conditioned paths
* `f`: a function that we want to process with ADAA
* `F1`: f's first antiderivative
* `F2`: f's second antiderivative
#### Test
```faust
aa = library("aanl.lib");
ba = library("basics.lib");
ma = library("maths.lib");
os = library("oscillators.lib");
ADAA2_test = aa.ADAA2(0.001, f, F1, F2, os.osc(110))
with {
f(x) = aa.clip(-1.0, 1.0, x);
F1(x) = ba.if((x <= 1.0) & (x >= -1.0), 0.5 * x^2, x * ma.signum(x) - 0.5);
F2(x) = ba.if((x <= 1.0) & (x >= -1.0), (1.0 / 3.0) * x^3, ((0.5 * x^2) - 1.0 / 6.0) * ma.signum(x));
};
```

---

## aa.hardclip

-------`(aa.)hardclip`---------------------
First-order ADAA hard-clip.
The domain of this function is ℝ; its theoretical range is [-1.0; 1.0].
#### Usage
```faust
_ : aa.hardclip : _
```
#### Test
```faust
aa = library("aanl.lib");
os = library("oscillators.lib");
hardclip_test = aa.hardclip(os.osc(110));
```

---

## aa.hardclip2

-------`(aa.)hardclip2`---------------------
Second-order ADAA hard-clip.
The domain of this function is ℝ; its theoretical range is [-1.0; 1.0].
#### Usage
```faust
_ : aa.hardclip2 : _
```
#### Test
```faust
aa = library("aanl.lib");
os = library("oscillators.lib");
hardclip2_test = aa.hardclip2(os.osc(110));
```

---

## aa.cubic1

-------`(aa.)cubic1`---------------------
First-order ADAA cubic saturator.
The domain of this function is ℝ; its theoretical range is
[-2.0/3.0; 2.0/3.0].
#### Usage
```faust
_ : aa.cubic1 : _
```
#### Test
```faust
aa = library("aanl.lib");
os = library("oscillators.lib");
cubic1_test = aa.cubic1(os.osc(110));
```

---

## aa.parabolic

-------`(aa.)parabolic`---------------------
First-order ADAA parabolic saturator.
The domain of this function is ℝ; its theoretical range is [-1.0; 1.0].
#### Usage
```faust
_ : aa.parabolic : _
```
#### Test
```faust
aa = library("aanl.lib");
os = library("oscillators.lib");
parabolic_test = aa.parabolic(os.osc(110));
```

---

## aa.parabolic2

-------`(aa.)parabolic2`---------------------
Second-order ADAA parabolic saturator.
The domain of this function is ℝ; its theoretical range is [-1.0; 1.0].
#### Usage
```faust
_ : aa.parabolic2 : _
```
#### Test
```faust
aa = library("aanl.lib");
os = library("oscillators.lib");
parabolic2_test = aa.parabolic2(os.osc(110));
```

---

## aa.hyperbolic

-------`(aa.)hyperbolic`---------------------
First-order ADAA hyperbolic saturator.
The domain of this function is ℝ; its theoretical range is [-1.0; 1.0].
#### Usage
```faust
_ : aa.hyperbolic : _
```
#### Test
```faust
aa = library("aanl.lib");
os = library("oscillators.lib");
hyperbolic_test = aa.hyperbolic(os.osc(110));
```

---

## aa.hyperbolic2

-------`(aa.)hyperbolic2`---------------------
Second-order ADAA hyperbolic saturator.
The domain of this function is ℝ; its theoretical range is [-1.0; 1.0].
#### Usage
```faust
_ : aa.hyperbolic2 : _
```
#### Test
```faust
aa = library("aanl.lib");
os = library("oscillators.lib");
hyperbolic2_test = aa.hyperbolic2(os.osc(110));
```

---

## aa.sinarctan

-------`(aa.)sinarctan`---------------------
First-order ADAA sin(atan()) saturator.
The domain of this function is ℝ; its theoretical range is [-1.0; 1.0].
#### Usage
```faust
_ : aa.sinarctan : _
```
#### Test
```faust
aa = library("aanl.lib");
os = library("oscillators.lib");
sinarctan_test = aa.sinarctan(os.osc(110));
```

---

## aa.sinarctan2

-------`(aa.)sinarctan2`---------------------
Second-order ADAA sin(atan()) saturator.
The domain of this function is ℝ; its theoretical range is [-1.0; 1.0].
#### Usage
```faust
_ : aa.sinarctan2 : _
```
#### Test
```faust
aa = library("aanl.lib");
os = library("oscillators.lib");
sinarctan2_test = aa.sinarctan2(os.osc(110));
```

---

## aa.softclipQuadratic1

-------`(aa.)softclipQuadratic1`---------------------
First-order ADAA quadratic softclip.
The domain of this function is ℝ; its theoretical range is [-1.0; 1.0].
#### Usage
```faust
_ : aa.softclipQuadratic1 : _
```
#### Test
```faust
aa = library("aanl.lib");
os = library("oscillators.lib");
softclipQuadratic1_test = aa.softclipQuadratic1(os.osc(110));
```

---

## aa.softclipQuadratic2

-------`(aa.)softclipQuadratic2`---------------------
Second-order ADAA quadratic softclip.
The domain of this function is ℝ; its theoretical range is [-1.0; 1.0].
#### Usage
```faust
_ : aa.softclipQuadratic2 : _
```
#### Test
```faust
aa = library("aanl.lib");
os = library("oscillators.lib");
softclipQuadratic2_test = aa.softclipQuadratic2(os.osc(110));
```

---

## aa.tanh1

-------`(aa.)tanh1`---------------------
First-order ADAA tanh() saturator.
The domain of this function is ℝ; its theoretical range is [-1.0; 1.0].
#### Usage
```faust
_ : aa.tanh1 : _
```
#### Test
```faust
aa = library("aanl.lib");
os = library("oscillators.lib");
tanh1_test = aa.tanh1(os.osc(110));
```

---

## aa.arctan

-------`(aa.)arctan`---------------------
First-order ADAA atan().
The domain of this function is ℝ; its theoretical range is [-π/2.0; π/2.0].
#### Usage
```faust
_ : aa.arctan : _
```
#### Test
```faust
aa = library("aanl.lib");
os = library("oscillators.lib");
arctan_test = aa.arctan(os.osc(110));
```

---

## aa.arctan2

-------`(aa.)arctan2`---------------------
Second-order ADAA atan().
The domain of this function is ℝ; its theoretical range is ]-π/2.0; π/2.0[.
#### Usage
```faust
_ : aa.arctan2 : _
```
#### Test
```faust
aa = library("aanl.lib");
os = library("oscillators.lib");
arctan2_test = aa.arctan2(os.osc(110));
```

---

## aa.asinh1

-------`(aa.)asinh1`---------------------
First-order ADAA asinh() saturator (unbounded).
The domain of this function is ℝ; its theoretical range is ℝ.
#### Usage
```faust
_ : aa.asinh1 : _
```
#### Test
```faust
aa = library("aanl.lib");
os = library("oscillators.lib");
asinh1_test = aa.asinh1(os.osc(110));
```

---

## aa.asinh2

-------`(aa.)asinh2`---------------------
Second-order ADAA asinh() saturator (unbounded).
The domain of this function is ℝ; its theoretical range is ℝ.
#### Usage
```faust
_ : aa.asinh2 : _
```
#### Test
```faust
aa = library("aanl.lib");
os = library("oscillators.lib");
asinh2_test = aa.asinh2(os.osc(110));
```

---

## aa.cosine1

-------`(aa.)cosine1`---------------------
First-order ADAA cos().
The domain of this function is ℝ; its theoretical range is [-1.0; 1.0].
#### Usage
```faust
_ : aa.cosine1 : _
```
#### Test
```faust
aa = library("aanl.lib");
os = library("oscillators.lib");
cosine1_test = aa.cosine1(os.osc(110));
```

---

## aa.cosine2

-------`(aa.)cosine2`---------------------
Second-order ADAA cos().
The domain of this function is ℝ; its theoretical range is [-1.0; 1.0].
#### Usage
```faust
_ : aa.cosine2 : _
```
#### Test
```faust
aa = library("aanl.lib");
os = library("oscillators.lib");
cosine2_test = aa.cosine2(os.osc(110));
```

---

## aa.arccos

-------`(aa.)arccos`---------------------
First-order ADAA acos().
The domain of this function is [-1.0; 1.0]; its theoretical range is
[π; 0.0].
#### Usage
```faust
_ : aa.arccos : _
```
#### Test
```faust
aa = library("aanl.lib");
os = library("oscillators.lib");
arccos_test = aa.arccos(os.osc(110));
```

---

## aa.arccos2

-------`(aa.)arccos2`---------------------
Second-order ADAA acos().
The domain of this function is [-1.0; 1.0]; its theoretical range is
[π; 0.0].
Note that this function is not accurate for low-amplitude or low-frequency
input signals. In that case, the first-order ADAA arccos() can be used.
#### Usage
```faust
_ : aa.arccos2 : _
```
#### Test
```faust
aa = library("aanl.lib");
os = library("oscillators.lib");
arccos2_test = aa.arccos2(os.osc(110));
```

---

## aa.acosh1

-------`(aa.)acosh1`---------------------
First-order ADAA acosh().
The domain of this function is ℝ >= 1.0; its theoretical range is ℝ >= 0.0.
#### Usage
```faust
_ : aa.acosh1 : _
```
#### Test
```faust
aa = library("aanl.lib");
os = library("oscillators.lib");
acosh1_test = aa.acosh1(1.0 + abs(os.osc(110)));
```

---

## aa.acosh2

-------`(aa.)acosh2`---------------------
Second-order ADAA acosh().
The domain of this function is ℝ >= 1.0; its theoretical range is ℝ >= 0.0.
Note that this function is not accurate for low-frequency input signals.
In that case, the first-order ADAA acosh() can be used.
#### Usage
```faust
_ : aa.acosh2 : _
```
#### Test
```faust
aa = library("aanl.lib");
os = library("oscillators.lib");
acosh2_test = aa.acosh2(1.0 + abs(os.osc(110)));
```

---

## aa.sine

-------`(aa.)sine`---------------------
First-order ADAA sin().
The domain of this function is ℝ; its theoretical range is ℝ.
#### Usage
```faust
_ : aa.sine : _
```
#### Test
```faust
aa = library("aanl.lib");
os = library("oscillators.lib");
sine_test = aa.sine(os.osc(110));
```

---

## aa.sine2

-------`(aa.)sine2`---------------------
Second-order ADAA sin().
The domain of this function is ℝ; its theoretical range is ℝ.
#### Usage
```faust
_ : aa.sine2 : _
```
#### Test
```faust
aa = library("aanl.lib");
os = library("oscillators.lib");
sine2_test = aa.sine2(os.osc(110));
```

---

## aa.arcsin

-------`(aa.)arcsin`---------------------
First-order ADAA asin().
The domain of this function is [-1.0, 1.0]; its theoretical range is
[-π/2.0; π/2.0].
#### Usage
```faust
_ : aa.arcsin : _
```
#### Test
```faust
aa = library("aanl.lib");
os = library("oscillators.lib");
arcsin_test = aa.arcsin(os.osc(110));
```

---

## aa.arcsin2

-------`(aa.)arcsin2`---------------------
Second-order ADAA asin().
The domain of this function is [-1.0, 1.0]; its theoretical range is
[-π/2.0; π/2.0].
Note that this function is not accurate for low-frequency input signals.
In that case, the first-order ADAA asin() can be used.
#### Usage
```faust
_ : aa.arcsin2 : _
```
#### Test
```faust
aa = library("aanl.lib");
os = library("oscillators.lib");
arcsin2_test = aa.arcsin2(os.osc(110));
```

---

## aa.tangent

-------`(aa.)tangent`---------------------
First-order ADAA tan().
The domain of this function is [-π/2.0; π/2.0]; its theoretical range is ℝ.
#### Usage
```faust
_ : aa.tangent : _
```
#### Test
```faust
aa = library("aanl.lib");
ma = library("maths.lib");
os = library("oscillators.lib");
tangent_test = aa.tangent(0.25 * ma.PI * os.osc(110));
```

---

## aa.atanh1

-------`(aa.)atanh1`---------------------
First-order ADAA atanh().
The domain of this function is [-1.0; 1.0]; its theoretical range is ℝ.
#### Usage
```faust
_ : aa.atanh1 : _
```
#### Test
```faust
aa = library("aanl.lib");
os = library("oscillators.lib");
atanh1_test = aa.atanh1(0.8 * os.osc(110));
```

---

## aa.atanh2

-------`(aa.)atanh2`---------------------
Second-order ADAA atanh().
The domain of this function is [-1.0; 1.0]; its theoretical range is ℝ.
#### Usage
```faust
_ : aa.atanh2 : _
```
#### Test
```faust
aa = library("aanl.lib");
os = library("oscillators.lib");
atanh2_test = aa.atanh2(0.8 * os.osc(110));
```

---

# all.lib
**Prefix:** `al`

##################################### all.lib ##########################################
The purpose of this library is to give access to all the Faust standard libraries
from a single point.
########################################################################################

# analyzers.lib
**Prefix:** `an`

################################ analyzers.lib ##########################################
Analyzers library. Its official prefix is `an`.

This library provides reusable building blocks for audio
signal *analysis* and metering. It includes functions and
components for measuring levels, extracting features, and
computing statistics useful in visualization, diagnostics,
adaptive processing, and music information retrieval.

The Analyzers library is organized into 7 sections:

* [Amplitude Tracking](#amplitude-tracking)
* [Adaptive Frequency Analysis](#adaptive-frequency-analysis)
* [Spectrum-Analyzers](#spectrum-analyzers)
* [Mth-Octave Spectral Level](#mth-octave-spectral-level)
* [Arbritary-Crossover Filter-Banks and Spectrum Analyzers](#arbritary-crossover-filter-banks-and-spectrum-analyzers)
* [Fast Fourier Transform (fft) and its Inverse (ifft)](#fast-fourier-transform-fft-and-its-inverse-ifft)
* [Test signal generators](#test-signal-generators)

#### References

* <https://github.com/grame-cncm/faustlibraries/blob/master/analyzers.lib>
########################################################################################

## an.abs_envelope_rect

------------------`(an.)abs_envelope_rect`-----------------------------------
Absolute value average with moving-average algorithm.
#### Usage
```faust
_ : abs_envelope_rect(period) : _
```
Where:
* `period`: sets the averaging frame in seconds
#### Test
```faust
an = library("analyzers.lib");
os = library("oscillators.lib");
abs_envelope_rect_test = an.abs_envelope_rect(0.05, os.osc(220));
```

---

## an.abs_envelope_tau

------------------`(an.)abs_envelope_tau`------------------------------------
Absolute value average with one-pole lowpass and tau response
(see [filters.lib](https://faustlibraries.grame.fr/libs/filters/)).
#### Usage
```faust
_ : abs_envelope_tau(period) : _
```
Where:
* `period`: (time to decay by 1/e) sets the averaging frame in secs
#### Test
```faust
an = library("analyzers.lib");
os = library("oscillators.lib");
abs_envelope_tau_test = an.abs_envelope_tau(0.05, os.osc(220));
```

---

## an.abs_envelope_t60

------------------`(an.)abs_envelope_t60`------------------------------------
Absolute value average with one-pole lowpass and t60 response
(see [filters.lib](https://faustlibraries.grame.fr/libs/filters/)).
#### Usage
```faust
_ : abs_envelope_t60(period) : _
```
Where:
* `period`: (time to decay by 60 dB) sets the averaging frame in secs
#### Test
```faust
an = library("analyzers.lib");
os = library("oscillators.lib");
abs_envelope_t60_test = an.abs_envelope_t60(0.05, os.osc(220));
```

---

## an.abs_envelope_t19

------------------`(an.)abs_envelope_t19`------------------------------------
Absolute value average with one-pole lowpass and t19 response
(see [filters.lib](https://faustlibraries.grame.fr/libs/filters/)).
#### Usage
```faust
_ : abs_envelope_t19(period) : _
```
Where:
* `period`: (time to decay by 1/e^2.2) sets the averaging frame in secs
#### Test
```faust
an = library("analyzers.lib");
os = library("oscillators.lib");
abs_envelope_t19_test = an.abs_envelope_t19(0.05, os.osc(220));
```

---

## an.amp_follower

---------------------------`(an.)amp_follower`---------------------------
Classic analog audio envelope follower with infinitely fast rise and
exponential decay.  The amplitude envelope instantaneously follows
the absolute value going up, but then floats down exponentially.
`amp_follower` is a standard Faust function.
#### Usage
```faust
_ : amp_follower(rel) : _
```
Where:
* `rel`: release time = amplitude-envelope time-constant (sec) going down
#### Test
```faust
an = library("analyzers.lib");
os = library("oscillators.lib");
amp_follower_test = os.osc(220) : an.amp_follower(0.05);
```
#### References
* Musical Engineer's Handbook, Bernie Hutchins, Ithaca NY
* 1975 Electronotes Newsletter, Bernie Hutchins

---

## an.amp_follower_ud

---------------------------`(an.)amp_follower_ud`---------------------------
Envelope follower with different up and down time-constants
(also called a "peak detector").
#### Usage
```faust
_ : amp_follower_ud(att,rel) : _
```
Where:
* `att`: attack time = amplitude-envelope time constant (sec) going up
* `rel`: release time = amplitude-envelope time constant (sec) going down
#### Test
```faust
an = library("analyzers.lib");
os = library("oscillators.lib");
amp_follower_ud_test = os.osc(220) : an.amp_follower_ud(0.002, 0.05);
```
#### Note
We assume rel >> att.  Otherwise, consider rel ~ max(rel,att).
For audio, att is normally faster (smaller) than rel (e.g., 0.001 and 0.01).
Use `amp_follower_ar` below to remove this restriction.
#### References
* "Digital Dynamic Range Compressor Design --- A Tutorial and Analysis", by
Dimitrios Giannoulis, Michael Massberg, and Joshua D. Reiss
<https://www.eecs.qmul.ac.uk/~josh/documents/2012/GiannoulisMassbergReiss-dynamicrangecompression-JAES2012.pdf>

---

## an.amp_follower_ar

---------------`(an.)amp_follower_ar`----------------
Envelope follower with independent attack and release times. The
release can be shorter than the attack (unlike in `amp_follower_ud`
above).
#### Usage
```faust
_ : amp_follower_ar(att,rel) : _
```
Where:
* `att`: attack time = amplitude-envelope time constant (sec) going up
* `rel`: release time = amplitude-envelope time constant (sec) going down
#### Test
```faust
an = library("analyzers.lib");
os = library("oscillators.lib");
amp_follower_ar_test = os.osc(220) : an.amp_follower_ar(0.002, 0.05);
```

---

## an.ms_envelope_rect

------------------`(an.)ms_envelope_rect`------------------------------------
Mean square with moving-average algorithm.
#### Usage
```faust
_ : ms_envelope_rect(period) : _
```
Where:
* `period`: sets the averaging frame in secs
#### Test
```faust
an = library("analyzers.lib");
os = library("oscillators.lib");
ms_envelope_rect_test = an.ms_envelope_rect(0.05, os.osc(220));
```

---

## an.ms_envelope_tau

------------------`(an.)ms_envelope_tau`-------------------------------------
Mean square average with one-pole lowpass and tau response
(see [filters.lib](https://faustlibraries.grame.fr/libs/filters/)).
#### Usage
```faust
_ : ms_envelope_tau(period) : _
```
Where:
* `period`: (time to decay by 1/e) sets the averaging frame in secs
#### Test
```faust
an = library("analyzers.lib");
os = library("oscillators.lib");
ms_envelope_tau_test = an.ms_envelope_tau(0.05, os.osc(220));
```

---

## an.ms_envelope_t60

------------------`(an.)ms_envelope_t60`-------------------------------------
Mean square with one-pole lowpass and t60 response
(see [filters.lib](https://faustlibraries.grame.fr/libs/filters/)).
#### Usage
```faust
_ : ms_envelope_t60(period) : _
```
Where:
* `period`: (time to decay by 60 dB) sets the averaging frame in secs
#### Test
```faust
an = library("analyzers.lib");
os = library("oscillators.lib");
ms_envelope_t60_test = an.ms_envelope_t60(0.05, os.osc(220));
```

---

## an.ms_envelope_t19

------------------`(an.)ms_envelope_t19`-------------------------------------
Mean square with one-pole lowpass and t19 response
(see [filters.lib](https://faustlibraries.grame.fr/libs/filters/)).
#### Usage
```faust
_ : ms_envelope_t19(period) : _
```
Where:
* `period`: (time to decay by 1/e^2.2) sets the averaging frame in secs
#### Test
```faust
an = library("analyzers.lib");
os = library("oscillators.lib");
ms_envelope_t19_test = an.ms_envelope_t19(0.05, os.osc(220));
```

---

## an.rms_envelope_rect

------------------`(an.)rms_envelope_rect`-----------------------------------
Root mean square with moving-average algorithm.
#### Usage
```faust
_ : rms_envelope_rect(period) : _
```
Where:
* `period`: sets the averaging frame in secs
#### Test
```faust
an = library("analyzers.lib");
os = library("oscillators.lib");
rms_envelope_rect_test = an.rms_envelope_rect(0.05, os.osc(220));
```

---

## an.rms_envelope_tau

------------------`(an.)rms_envelope_tau`------------------------------------
Root mean square with one-pole lowpass and tau response
(see [filters.lib](https://faustlibraries.grame.fr/libs/filters/)).
#### Usage
```faust
_ : rms_envelope_tau(period) : _
```
Where:
* `period`: (time to decay by 1/e) sets the averaging frame in secs
#### Test
```faust
an = library("analyzers.lib");
os = library("oscillators.lib");
rms_envelope_tau_test = an.rms_envelope_tau(0.05, os.osc(220));
```

---

## an.rms_envelope_t60

------------------`(an.)rms_envelope_t60`------------------------------------
Root mean square with one-pole lowpass and t60 response
(see [filters.lib](https://faustlibraries.grame.fr/libs/filters/)).
#### Usage
```faust
_ : rms_envelope_t60(period) : _
```
Where:
* `period`: (time to decay by 60 dB) sets the averaging frame in secs
#### Test
```faust
an = library("analyzers.lib");
os = library("oscillators.lib");
rms_envelope_t60_test = an.rms_envelope_t60(0.05, os.osc(220));
```

---

## an.rms_envelope_t19

------------------`(an.)rms_envelope_t19`------------------------------------
Root mean square with one-pole lowpass and t19 response
(see [filters.lib](https://faustlibraries.grame.fr/libs/filters/)).
#### Usage
```faust
_ : rms_envelope_t19(period) : _
```
Where:
* `period`: (time to decay by 1/e^2.2) sets the averaging frame in secs
#### Test
```faust
an = library("analyzers.lib");
os = library("oscillators.lib");
rms_envelope_t19_test = an.rms_envelope_t19(0.05, os.osc(220));
```

---

## an.zcr

-----------------------`(an.)zcr`--------------------------------------------
Zero-crossing rate (ZCR) with one-pole lowpass averaging based on the tau
constant. It outputs an index between 0 and 1 at a desired analysis frame.
The ZCR of a signal correlates with the noisiness [Gouyon et al. 2000] and
the spectral centroid [Herrera-Boyer et al. 2006] of a signal.
For sinusoidal signals, the ZCR can be multiplied by ma.SR/2 and used
as a frequency detector. For example, it can be deployed as a
computationally efficient adaptive mechanism for automatic Larsen
suppression.
#### Usage
```faust
_ : zcr(tau) : _
```
Where:
* `tau`: (time to decay by e^-1) sets the averaging frame in seconds.
#### Test
```faust
an = library("analyzers.lib");
os = library("oscillators.lib");
zcr_test = an.zcr(0.01, os.osc(220));
```

---

## an.pitchTracker

--------------------`(an.)pitchTracker`---------------------------------------
This function implements a pitch-tracking algorithm by means of
zero-crossing rate analysis and adaptive low-pass filtering. The design
is based on the algorithm described in [this tutorial (section 2.2)](https://github.com/grame-cncm/faust/blob/master-dev/documentation/misc/Faust_tutorial2.pdf).
#### Usage
```faust
_ : pitchTracker(N, tau) : _
```
Where:
* `N`: a constant numerical expression, sets the order of the low-pass filter, which
determines the sensitivity of the algorithm for signals where partials are
stronger than the fundamental frequency.
* `tau`: response time in seconds based on exponentially-weighted averaging with tau time-constant. See <https://ccrma.stanford.edu/~jos/st/Exponentials.html>.
#### Test
```faust
an = library("analyzers.lib");
os = library("oscillators.lib");
pitchTracker_test = an.pitchTracker(4, 0.02, os.osc(220));
```

---

## an.spectralCentroid

--------------------`(an.)spectralCentroid`-----------------------------------
This function implements a time-domain spectral centroid by means of RMS
measurements and adaptive crossover filtering. The weight difference of the
upper and lower spectral powers are used to recursively adjust the crossover
cutoff so that the system (minimally) oscillates around a balancing point.
Unlike block processing techniques such as FFT, this algorithm provides
continuous measurements and fast response times. Furthermore, when providing
input signals that are spectrally sparse, the algorithm will output a
logarithmic measure of the centroid, which is perceptually desirable for
musical applications. For example, if the input signal is the combination
of three tones at 1000, 2000, and 4000 Hz, the centroid will be the middle
octave.
#### Usage
```faust
_ : spectralCentroid(nonlinearity, tau) : _
```
Where:
* `nonlinearity`: a boolean to activate or deactivate nonlinear integration. The
nonlinear function is useful to improve stability with very short response times
such as .001 <= tau <= .005 , otherwise, the nonlinearity may reduce precision.
* `tau`: response time in seconds based on exponentially-weighted averaging with tau time-constant. See <https://ccrma.stanford.edu/~jos/st/Exponentials.html>.
#### Example:
`process = os.osc(500) + os.osc(1000) + os.osc(2000) + os.osc(4000) + os.osc(8000) : an.spectralCentroid(1, .001);`
#### Test
```faust
an = library("analyzers.lib");
os = library("oscillators.lib");
spectralCentroid_test = (os.osc(440) + os.osc(880)) : an.spectralCentroid(1, 0.01);
```
#### References
Sanfilippo, D. (2021). Time-Domain Adaptive Algorithms for Low- and High-Level
Audio Information Processing. Computer Music Journal, 45(1), 24-38.

---

## an.mth_octave_analyzer

-------------------------`(an.)mth_octave_analyzer`----------------------------
Octave analyzer.
`mth_octave_analyzer[N]` are standard Faust functions.
#### Usage
```faust
_ : mth_octave_analyzer(O,M,ftop,N) : par(i,N,_) // Oth-order Butterworth
_ : mth_octave_analyzer6e(M,ftop,N) : par(i,N,_) // 6th-order elliptic
```
Also for convenience:
```faust
_ : mth_octave_analyzer3(M,ftop,N) : par(i,N,_) // 3d-order Butterworth
_ : mth_octave_analyzer5(M,ftop,N) : par(i,N,_) // 5th-order Butterworth
mth_octave_analyzer_default = mth_octave_analyzer6e;
```
Where:
* `O`: (odd) order of filter used to split each frequency band into two
* `M`: number of band-slices per octave
* `ftop`: highest band-split crossover frequency (e.g., 20 kHz)
* `N`: total number of bands (including dc and Nyquist)
#### Test
```faust
an = library("analyzers.lib");
os = library("oscillators.lib");
mth_octave_analyzer_test = os.osc(440) : an.mth_octave_analyzer(3, 3, 8000, 5);
```

---

## an.mth_octave_spectral_level6e

------------------------`(an.)mth_octave_spectral_level6e`-------------------------
Spectral level display.
#### Usage:
```faust
_ : mth_octave_spectral_level6e(M,ftop,NBands,tau,dB_offset) : _
```
Where:
* `M`: bands per octave
* `ftop`: lower edge frequency of top band
* `NBands`: number of passbands (including highpass and dc bands),
* `tau`: spectral display averaging-time (time constant) in seconds,
* `dB_offset`: constant dB offset in all band level meters.
Also for convenience:
```faust
mth_octave_spectral_level_default = mth_octave_spectral_level6e;
spectral_level = mth_octave_spectral_level(2,10000,20);
```
#### Test
```faust
an = library("analyzers.lib");
os = library("oscillators.lib");
mth_octave_spectral_level6e_test = os.osc(440) : an.mth_octave_spectral_level6e(3, 8000, 5, 0.05, 0);
```

---

## an.analyzer

---------------`(an.)analyzer`--------------------------
Analyzer.
#### Usage
```faust
_ : analyzer(O,freqs) : par(i,N,_) // No delay equalizer
```
Where:
* `O`: band-split filter order (ODD integer required for filterbank[i])
* `freqs`: (fc1,fc2,...,fcNs) [in numerically ascending order], where
Ns=N-1 is the number of octave band-splits
(total number of bands N=Ns+1).
If frequencies are listed explicitly as arguments, enclose them in parens:
```faust
_ : analyzer(3,(fc1,fc2)) : _,_,_
```
#### Test
```faust
an = library("analyzers.lib");
os = library("oscillators.lib");
analyzer_test = os.osc(440) : an.analyzer(3, (500, 2000));
```

---

## an.ifft

---------------`(an.)ifft`--------------------------
Inverse Fast Fourier Transform (IFFT).
#### Usage
```faust
si.cbus(N) : ifft(N) : si.cbus(N)
```
Where:
* N is the IFFT size (power of 2)
* Input is a complex spectrum represented as interleaved real and imaginary parts:
(R0, I0), (R1,I1), (R2,I2), ...
* Output is a bank of N complex signals giving the complex signal in the time domain:
(r0, i0), (r1,i1), (r2,i2), ...
#### Test
```faust
an = library("analyzers.lib");
os = library("oscillators.lib");
ifft_test = (an.rtocv(8, os.osc(220)) : an.fft(8)) : an.ifft(8);
```

---

## an.logsweep

---------------`(an.)logsweep`---------------------
Logarithmic sine sweep generator.
#### Usage
```faust
logsweep(fs,fe,dur) : _
```
Where:
* `fs`: start frequency in Hz
* `fe`: end frequency in Hz
* `dur`: duration of the sweep in seconds
#### Test
```faust
an = library("analyzers.lib");
logsweep_test = an.logsweep(20, 2000, 5);
```

---

## an.linsweep

---------------`(an.)linsweep`---------------------
Linear sine sweep generator.
#### Usage
```faust
linsweep(fs,fe,dur) : _
```
Where:
* `fs`: start frequency in Hz
* `fe`: end frequency in Hz
* `dur`: duration of the sweep in seconds
#### Test
```faust
an = library("analyzers.lib");
linsweep_test = an.linsweep(20, 2000, 5);
```

---

# basics.lib
**Prefix:** `ba`

################################ basics.lib ##########################################
Basics library. Its official prefix is `ba`.

This library provides reusable building blocks for core DSP and Faust
programming. It typically includes low-level utilities for math, routing,
signal conditioning, timing, control, and helper components used across
higher-level libraries.

The Basics library is organized into 8 sections:

* [Conversion Tools](#conversion-tools)
* [Counters and Time/Tempo Tools](#counters-and-timetempo-tools)
* [Array Processing/Pattern Matching](#array-processingpattern-matching)
* [Function tabulation](#function-tabulation)
* [Selectors (Conditions)](#selectors-conditions)
* [Other](#other)
* [Sliding Reduce](#sliding-reduce)
* [Parallel Operators](#parallel-operators)

#### References

* <https://github.com/grame-cncm/faustlibraries/blob/master/basics.lib>
########################################################################################

## ba.samp2sec

-------`(ba.)samp2sec`----------
Converts a number of samples to a duration in seconds at the current sampling rate (see `ma.SR`).
`samp2sec` is a standard Faust function.
#### Usage
```faust
samp2sec(n) : _
```
Where:
* `n`: number of samples
#### Test
```faust
ba = library("basics.lib");
samp2sec_test = ba.samp2sec(512);
```

---

## ba.sec2samp

-------`(ba.)sec2samp`----------
Converts a duration in seconds to a number of samples at the current sampling rate (see `ma.SR`).
`samp2sec` is a standard Faust function.
#### Usage
```faust
sec2samp(d) : _
```
Where:
* `d`: duration in seconds
#### Test
```faust
ba = library("basics.lib");
sec2samp_test = ba.sec2samp(0.01);
```

---

## ba.db2linear

-------`(ba.)db2linear`----------
dB-to-linear value converter. It can be used to convert an amplitude in dB to a linear gain ]0-N].
`db2linear` is a standard Faust function.
#### Usage
```faust
db2linear(l) : _
```
Where:
* `l`: amplitude in dB
#### Test
```faust
ba = library("basics.lib");
db2linear_test = ba.db2linear(-6);
```

---

## ba.linear2db

-------`(ba.)linear2db`----------
linea-to-dB value converter. It can be used to convert a linear gain ]0-N] to an amplitude in dB.
`linear2db` is a standard Faust function.
#### Usage
```faust
linear2db(g) : _
```
Where:
* `g`: a linear gain
#### Test
```faust
ba = library("basics.lib");
linear2db_test = ba.linear2db(0.5);
```

---

## ba.lin2LogGain

----------`(ba.)lin2LogGain`------------------
Converts a linear gain (0-1) to a log gain (0-1).
#### Usage
```faust
lin2LogGain(n) : _
```
Where:
* `n`: the linear gain
#### Test
```faust
ba = library("basics.lib");
lin2LogGain_test = ba.lin2LogGain(0.5);
```

---

## ba.log2LinGain

----------`(ba.)log2LinGain`------------------
Converts a log gain (0-1) to a linear gain (0-1).
#### Usage
```faust
log2LinGain(n) : _
```
Where:
* `n`: the log gain
#### Test
```faust
ba = library("basics.lib");
log2LinGain_test = ba.log2LinGain(0.25);
```

---

## ba.tau2pole

-------`(ba.)tau2pole`----------
Returns a real pole giving exponential decay.
Note that t60 (time to decay 60 dB) is ~6.91 time constants.
`tau2pole` is a standard Faust function.
#### Usage
```faust
_ : smooth(tau2pole(tau)) : _
```
Where:
* `tau`: time-constant in seconds
tau2pole(tau) = exp(-1.0/(tau*ma.SR));
#### Test
```faust
ba = library("basics.lib");
tau2pole_test = ba.tau2pole(0.01);
```

---

## ba.pole2tau

-------`(ba.)pole2tau`----------
Returns the time-constant, in seconds, corresponding to the given real,
positive pole in (0-1).
`pole2tau` is a standard Faust function.
#### Usage
```faust
pole2tau(pole) : _
```
Where:
* `pole`: the pole
#### Test
```faust
ba = library("basics.lib");
pole2tau_test = ba.pole2tau(0.9);
```

---

## ba.midikey2hz

-------`(ba.)midikey2hz`----------
Converts a MIDI key number to a frequency in Hz (MIDI key 69 = A440).
`midikey2hz` is a standard Faust function.
#### Usage
```faust
midikey2hz(mk) : _
```
Where:
* `mk`: the MIDI key number
#### Test
```faust
ba = library("basics.lib");
midikey2hz_test = ba.midikey2hz(60);
```

---

## ba.hz2midikey

-------`(ba.)hz2midikey`----------
Converts a frequency in Hz to a MIDI key number (MIDI key 69 = A440).
`hz2midikey` is a standard Faust function.
#### Usage
```faust
hz2midikey(freq) : _
```
Where:
* `freq`: frequency in Hz
#### Test
```faust
ba = library("basics.lib");
hz2midikey_test = ba.hz2midikey(440);
```

---

## ba.semi2ratio

-------`(ba.)semi2ratio`----------
Converts semitones in a frequency multiplicative ratio.
`semi2ratio` is a standard Faust function.
#### Usage
```faust
semi2ratio(semi) : _
```
Where:
* `semi`: number of semitone
#### Test
```faust
ba = library("basics.lib");
semi2ratio_test = ba.semi2ratio(7);
```

---

## ba.ratio2semi

-------`(ba.)ratio2semi`----------
Converts a frequency multiplicative ratio in semitones.
`ratio2semi` is a standard Faust function.
#### Usage
```faust
ratio2semi(ratio) : _
```
Where:
* `ratio`: frequency multiplicative ratio
#### Test
```faust
ba = library("basics.lib");
ratio2semi_test = ba.ratio2semi(2.0);
```

---

## ba.cent2ratio

-------`(ba.)cent2ratio`----------
Converts cents in a frequency multiplicative ratio.
#### Usage
```faust
cent2ratio(cent) : _
```
Where:
* `cent`: number of cents
#### Test
```faust
ba = library("basics.lib");
cent2ratio_test = ba.cent2ratio(100);
```

---

## ba.ratio2cent

-------`(ba.)ratio2cent`----------
Converts a frequency multiplicative ratio in cents.
#### Usage
```faust
ratio2cent(ratio) : _
```
Where:
* `ratio`: frequency multiplicative ratio
#### Test
```faust
ba = library("basics.lib");
ratio2cent_test = ba.ratio2cent(1.5);
```

---

## ba.pianokey2hz

-------`(ba.)pianokey2hz`----------
Converts a piano key number to a frequency in Hz (piano key 49 = A440).
#### Usage
```faust
pianokey2hz(pk) : _
```
Where:
* `pk`: the piano key number
#### Test
```faust
ba = library("basics.lib");
pianokey2hz_test = ba.pianokey2hz(49);
```

---

## ba.hz2pianokey

-------`(ba.)hz2pianokey`----------
Converts a frequency in Hz to a piano key number (piano key 49 = A440).
#### Usage
```faust
hz2pianokey(freq) : _
```
Where:
* `freq`: frequency in Hz
#### Test
```faust
ba = library("basics.lib");
hz2pianokey_test = ba.hz2pianokey(440);
```

---

## ba.counter

----------------------------`(ba.)counter`------------------------------
Starts counting 0, 1, 2, 3..., and raise the current integer value
at each upfront of the trigger.
#### Usage
```faust
counter(trig) : _
```
Where:
* `trig`: the trigger signal, each upfront will move the counter to the next integer
#### Test
```faust
ba = library("basics.lib");
counter_test = ba.counter(button("trig"));
```

---

## ba.countdown

----------------------------`(ba.)countdown`------------------------------
Starts counting down from n included to 0. While trig is 1 the output is n.
The countdown starts with the transition of trig from 1 to 0. At the end
of the countdown the output value will remain at 0 until the next trig.
`countdown` is a standard Faust function.
#### Usage
```faust
countdown(n,trig) : _
```
Where:
* `n`: the starting point of the countdown
* `trig`: the trigger signal (1: start at `n`; 0: decrease until 0)
#### Test
```faust
ba = library("basics.lib");
countdown_test = ba.countdown(8, button("trig"));
```

---

## ba.countup

----------------------------`(ba.)countup`--------------------------------
Starts counting up from 0 to n included. While trig is 1 the output is 0.
The countup starts with the transition of trig from 1 to 0. At the end
of the countup the output value will remain at n until the next trig.
`countup` is a standard Faust function.
#### Usage
```faust
countup(n,trig) : _
```
Where:
* `n`: the maximum count value
* `trig`: the trigger signal (1: start at 0; 0: increase until `n`)
#### Test
```faust
ba = library("basics.lib");
countup_test = ba.countup(8, button("trig"));
```

---

## ba.sweep

--------------------`(ba.)sweep`--------------------------
Counts from 0 to `period-1` repeatedly, generating a
sawtooth waveform, like `os.lf_rawsaw`,
starting at 1 when `run` transitions from 0 to 1.
Outputs zero while `run` is 0.
#### Usage
```faust
sweep(period,run) : _
```
#### Test
```faust
ba = library("basics.lib");
sweep_test = ba.sweep(64, checkbox("run"));
```

---

## ba.time

-------`(ba.)time`----------
A simple counter that produces the sequence of 0,1,2...N integer values.
`time` is a standard Faust function.
#### Usage
```faust
time : _
```
#### Test
```faust
ba = library("basics.lib");
time_test = ba.time;
```

---

## ba.ramp

-------`(ba.)ramp`----------
A linear ramp with a slope of '(+/-)1/n' samples to reach the next target value.
#### Usage
```faust
_ : ramp(n) : _
```
Where:
* `n`: number of samples to increment/decrement the value by one
#### Test
```faust
ba = library("basics.lib");
os = library("oscillators.lib");
ramp_test = os.osc(1) : ba.ramp(256);
```

---

## ba.line

-------`(ba.)line`----------
A ramp interpolator that generates a linear transition to reach a target value:
- the interpolation process restarts each time a new and distinct input value is received
- it utilizes 'n' samples to achieve the transition to the target value
- after reaching the target value, the output value is maintained.
#### Usage
```faust
_ : line(n) : _
```
Where:
* `n`: number of samples to reach the new target received at its input
#### Test
```faust
ba = library("basics.lib");
os = library("oscillators.lib");
line_test = os.osc(1) : ba.line(256);
```

---

## ba.tempo

-------`(ba.)tempo`----------
Converts a tempo in BPM into a number of samples.
#### Usage
```faust
tempo(t) : _
```
Where:
* `t`: tempo in BPM
#### Test
```faust
ba = library("basics.lib");
tempo_test = ba.tempo(120);
```

---

## ba.period

-------`(ba.)period`----------
Basic sawtooth wave of period `p`.
#### Usage
```faust
period(p) : _
```
Where:
* `p`: period as a number of samples
NOTE: may be this should go in oscillators.lib
#### Test
```faust
ba = library("basics.lib");
period_test = ba.period(64);
```

---

## ba.spulse

-------`(ba.)spulse`----------
Produces a single pulse of n samples when trig goes from 0 to 1.
#### Usage
```faust
spulse(n,trig) : _
```
Where:
* `n`: pulse length as a number of samples
* `trig`: the trigger signal (1: start the pulse)
#### Test
```faust
ba = library("basics.lib");
spulse_test = ba.spulse(32, button("trig"));
```

---

## ba.pulse

-------`(ba.)pulse`----------
Pulses (like 10000) generated at period `p`.
#### Usage
```faust
pulse(p) : _
```
Where:
* `p`: period as a number of samples
NOTE: may be this should go in oscillators.lib
#### Test
```faust
ba = library("basics.lib");
pulse_test = ba.pulse(64);
```

---

## ba.pulsen

-------`(ba.)pulsen`----------
Pulses (like 11110000) of length `n` generated at period `p`.
#### Usage
```faust
pulsen(n,p) : _
```
Where:
* `n`: pulse length as a number of samples
* `p`: period as a number of samples
NOTE: may be this should go in oscillators.lib
#### Test
```faust
ba = library("basics.lib");
pulsen_test = ba.pulsen(8, 64);
```

---

## ba.cycle

-----------------------`(ba.)cycle`---------------------------
Split nonzero input values into `n` cycles.
#### Usage
```faust
_ : cycle(n) : si.bus(n)
```
Where:
* `n`: the number of cycles/output signals
#### Test
```faust
ba = library("basics.lib");
cycle_test = button("gate") : ba.cycle(3);
```

---

## ba.beat

-------`(ba.)beat`----------
Pulses at tempo `t` in BPM.
`beat` is a standard Faust function.
#### Usage
```faust
beat(t) : _
```
Where:
* `t`: tempo in BPM
#### Test
```faust
ba = library("basics.lib");
beat_test = ba.beat(120);
```

---

## ba.pulse_countup

----------------------------`(ba.)pulse_countup`-----------------------------------
Starts counting up pulses. While trig is 1 the output is
counting up, while trig is 0 the counter is reset to 0.
#### Usage
```faust
_ : pulse_countup(trig) : _
```
Where:
* `trig`: the trigger signal (1: start at next pulse; 0: reset to 0)
#### Test
```faust
ba = library("basics.lib");
pulse_countup_test = ba.pulse_countup(button("run"));
```

---

## ba.pulse_countdown

----------------------------`(ba.)pulse_countdown`---------------------------------
Starts counting down pulses. While trig is 1 the output is
counting down, while trig is 0 the counter is reset to 0.
#### Usage
```faust
_ : pulse_countdown(trig) : _
```
Where:
* `trig`: the trigger signal (1: start at next pulse; 0: reset to 0)
#### Test
```faust
ba = library("basics.lib");
pulse_countdown_test = ba.pulse_countdown(button("run"));
```

---

## ba.pulse_countup_loop

----------------------------`(ba.)pulse_countup_loop`------------------------------
Starts counting up pulses from 0 to n included. While trig is 1 the output is
counting up, while trig is 0 the counter is reset to 0. At the end
of the countup (n) the output value will be reset to 0.
#### Usage
```faust
_ : pulse_countup_loop(n,trig) : _
```
Where:
* `n`: the highest number of the countup (included) before reset to 0
* `trig`: the trigger signal (1: start at next pulse; 0: reset to 0)
#### Test
```faust
ba = library("basics.lib");
pulse_countup_loop_test = ba.pulse_countup_loop(4, button("run"));
```

---

## ba.pulse_countdown_loop

----------------------------`(ba.)pulse_countdown_loop`----------------------------
Starts counting down pulses from 0 to n included. While trig is 1 the output
is counting down, while trig is 0 the counter is reset to 0. At the end
of the countdown (n) the output value will be reset to 0.
#### Usage
```faust
_ : pulse_countdown_loop(n,trig) : _
```
Where:
* `n`: the highest number of the countup (included) before reset to 0
* `trig`: the trigger signal (1: start at next pulse; 0: reset to 0)
#### Test
```faust
ba = library("basics.lib");
pulse_countdown_loop_test = ba.pulse_countdown_loop(4, button("run"));
```

---

## ba.resetCtr

-----------------------`(ba.)resetCtr`------------------------
Function that lets through the mth impulse out of
each consecutive group of `n` impulses.
#### Usage
```faust
_ : resetCtr(n,m) : _
```
Where:
* `n`: the total number of impulses being split
* `m`: index of impulse to allow to be output
#### Test
```faust
ba = library("basics.lib");
resetCtr_test = ba.pulse(16) : ba.resetCtr(4, 2);
```

---

## ba.count

---------------------------------`(ba.)count`---------------------------------
Count the number of elements of list l.
`count` is a standard Faust function.
#### Usage
```faust
count(l)
count((10,20,30,40)) -> 4
```
Where:
* `l`: list of elements
#### Test
```faust
ba = library("basics.lib");
count_test = ba.count((10,20,30,40));
```

---

## ba.take

-------------------------------`(ba.)take`-----------------------------------
Take an element from a list.
`take` is a standard Faust function.
#### Usage
```faust
take(P,l)
take(3,(10,20,30,40)) -> 30
```
Where:
* `P`: position (int, known at compile time, P > 0)
* `l`: list of elements
#### Test
```faust
ba = library("basics.lib");
take_test = ba.take(3, (10,20,30,40));
```

---

## ba.pick

-------------------------------`(ba.)pick`-----------------------------------
Pick the nth element from a list.
Similar to `ba.take(n+1,l)` but faster and more powerful.
#### Usage
```faust
pick(l,n) : _
```
Where:
* `l`: list of elements
* `n`: index of element to pick, compile time constant.
if n < 0 or n >= length of `l`, `pick()` outputs 0.
#### Example test program
```faust
pick((10,20,30,40), 2) -> 30
```
```faust
pick(si.bus(3), 1) // same as !,_,!
```
while `ba.take(2, si.bus(3))` acts as `_`.
Unlike `take()`, `pick()` always flattens the list, so
`pick((10,(20,30),40), 1)` outputs `20`, not `20,30`.
#### Test
```faust
ba = library("basics.lib");
pick_test = ba.pick((10,20,30,40), 2);
```

---

## ba.pickN

-------------------------------`(ba.)pickN`----------------------------------
Select the inputs listed in `O` among `N` at compile time.
#### Usage
```faust
si.bus(N) : pickN(N,O) : si.bus(outputs(O))
```
Where:
* `N`: number of inputs, compile time constant
* `O`: list of the inputs to select, compile time constants
#### Example test program
```faust
pickN(4,2) : _  // same as selector(2,4) but faster
```
```faust
pick(4,(1,3)) : _,_ // same as !,_,!,_
```
```faust
pickN(4,(1,3), (10,20,30,40)) -> (20,40)
```
```faust
process = pickN(2, (1,0,0,1)) // same as `process(x,y) = y,x,x,y`
```
#### Test
```faust
ba = library("basics.lib");
pickN_test = (1,2,3,4) : ba.pickN(4, (0,2));
```

---

## ba.subseq

----------------------------`(ba.)subseq`--------------------------------
Extract a part of a list.
#### Usage
```faust
subseq(l, P, N)
subseq((10,20,30,40,50,60), 1, 3) -> (20,30,40)
subseq((10,20,30,40,50,60), 4, 1) -> 50
```
Where:
* `l`: list
* `P`: start point (int, known at compile time, 0: begin of list)
* `N`: number of elements (int, known at compile time)
#### Note:
Faust doesn't have proper lists. Lists are simulated with parallel
compositions and there is no empty list.
#### Test
```faust
ba = library("basics.lib");
subseq_test = ba.subseq((10,20,30,40,50), 1, 3);
```

---

## ba.tabulate

-------`(ba.)tabulate`----------
Tabulate a 1D function over the range [r0, r1] for access via nearest-value, linear, cubic interpolation.
In other words, the uniformly tabulated function can be evaluated using interpolation of order 0 (none), 1 (linear), or 3 (cubic).
#### Usage
```faust
tabulate(C, FX, S, r0, r1, x).(val|lin|cub) : _
```
* `C`: whether to dynamically force the `x` value to the range [r0, r1]: 1 forces the check, 0 deactivates it (constant numerical expression)
* `FX`: unary function Y=F(X) with one output (scalar function of one variable)
* `S`: size of the table in samples (constant numerical expression)
* `r0`: minimum value of argument x
* `r1`: maximum value of argument x
```faust
tabulate(C, FX, S, r0, r1, x).val uses the value in the table closest to x
```
```faust
tabulate(C, FX, S, r0, r1, x).lin evaluates at x using linear interpolation between the closest stored values
```
```faust
tabulate(C, FX, S, r0, r1, x).cub evaluates at x using cubic interpolation between the closest stored values
```
#### Example test program
```faust
midikey2hz(mk) = ba.tabulate(1, ba.midikey2hz, 512, 0, 127, mk).lin;
process = midikey2hz(ba.time), ba.midikey2hz(ba.time);
```
#### Test
```faust
ba = library("basics.lib");
tabulate_test = ba.tabulate(1, ba.midikey2hz, 128, 0, 127, 60).lin;
```

---

## ba.tabulate_chebychev

-------`(ba.)tabulate_chebychev`----------
Tabulate a 1D function over the range [r0, r1] for access via Chebyshev polynomial approximation.
In contrast to `(ba.)tabulate`, which interpolates only between tabulated samples, `(ba.)tabulate_chebychev`
stores coefficients of Chebyshev polynomials that are evaluated to provide better approximations in many cases.
Two new arguments controlling this are NX, the number of segments into which [r0, r1] is divided, and CD,
the maximum Chebyshev polynomial degree to use for each segment. A `rdtable` of size NX*(CD+1) is internally used.
Note that processing `r1` the last point in the interval is not safe. So either be sure the input stays in [r0, r1[
or use `C = 1`.
#### Usage
```faust
_ : tabulate_chebychev(C, FX, NX, CD, r0, r1) : _
```
* `C`: whether to dynamically force the value to the range [r0, r1]: 1 forces the check, 0 deactivates it (constant numerical expression)
* `FX`: unary function Y=F(X) with one output (scalar function of one variable)
* `NX`: number of segments for uniformly partitioning [r0, r1] (constant numerical expression)
* `CD`: maximum polynomial degree for each Chebyshev polynomial (constant numerical expression)
* `r0`: minimum value of argument x
* `r1`: maximum value of argument x
#### Example test program
```faust
midikey2hz_chebychev(mk) = ba.tabulate_chebychev(1, ba.midikey2hz, 100, 4, 0, 127, mk);
process = midikey2hz_chebychev(ba.time), ba.midikey2hz(ba.time);
```
#### Test
```faust
ba = library("basics.lib");
tabulate_chebychev_test = ba.tabulate_chebychev(1, ba.midikey2hz, 32, 4, 0, 127, 60);
```

---

## ba.tabulateNd

-------`(ba.)tabulateNd`----------
Tabulate an nD function for access via nearest-value or linear or cubic interpolation. In other words, the tabulated function can be evaluated using interpolation of order 0 (none), 1 (linear), or 3 (cubic).
The table size and parameter range of each dimension can and must be separately specified. You can use it anywhere you have an expensive function with multiple parameters with known ranges. You could use it to build a wavetable synth, for example.
The number of dimensions is deduced from the number of parameters you give, see below.
Note that processing the last point in each interval is not safe. So either be sure the inputs stay in their respective ranges, or use `C = 1`. Similarly for the first point when doing cubic interpolation.
#### Usage
```faust
tabulateNd(C, function, (parameters) ).(val|lin|cub) : _
```
* `C`: whether to dynamically force the parameter values for each dimension to the ranges specified in parameters: 1 forces the check, 0 deactivates it (constant numerical expression)
* `function`: the function we want to tabulate. Can have any number of inputs, but needs to have just one output.
* `(parameters)`: sizes, ranges and read values. Note: these need to be in brackets, to make them one entity.
If N is the number of dimensions, we need:
* N times `S`: number of values to store for this dimension (constant numerical expression)
* N times `r0`: minimum value of this dimension
* N times `r1`: maximum value of this dimension
* N times `x`: read value of this dimension
By providing these parameters, you indirectly specify the number of dimensions; it's the number of parameters divided by 4.
The user facing functions are:
```faust
tabulateNd(C, function, S, parameters).val
```
- Uses the value in the table closest to x.
```faust
tabulateNd(C, function, S, parameters).lin
```
- Evaluates at x using linear interpolation between the closest stored values.
```faust
tabulateNd(C, function, S, parameters).cub
```
- Evaluates at x using cubic interpolation between the closest stored values.
#### Example test program
```faust
powSin(x,y) = sin(pow(x,y)); // The function we want to tabulate
powSinTable(x,y) = ba.tabulateNd(1, powSin, (sizeX,sizeY, rx0,ry0, rx1,ry1, x,y) ).lin;
sizeX = 512; // table size of the first parameter
sizeY = 512; // table size of the second parameter
rx0 = 2; // start of the range of the first parameter
ry0 = 2; // start of the range of the second parameter
rx1 = 10; // end of the range of the first parameter
ry1 = 10; // end of the range of the second parameter
x = hslider("x", rx0, rx0, rx1, 0.001):si.smoo;
y = hslider("y", ry0, ry0, ry1, 0.001):si.smoo;
process = powSinTable(x,y), powSin(x,y);
```
#### Working principle
The ``.val`` function just outputs the closest stored value.
The ``.lin`` and ``.cub`` functions interpolate in N dimensions.
##### Multi dimensional interpolation
To understand what it means to interpolate in N dimensions, here's a quick reminder on the general principle of 2D linear interpolation:
* We have a grid of values, and we want to find the value at a point (x, y) within this grid.
* We first find the four closest points (A, B, C, D) in the grid surrounding the point (x, y).
Then, we perform linear interpolation in the x-direction between points A and B, and between points C and D. This gives us two new points E and F. Finally, we perform linear interpolation in the y-direction between points E and F to get our value.
To implement this in Faust, we need N sequential groups of interpolators, where N is the number of dimensions.
Each group feeds into the next, with the last "group" being a single interpolator, and the group before it containing one interpolator for each input of the group it's feeding.
Some examples:
* Our 2D linear example has two interpolators feeding into one.
* A 3D linear interpolator has four interpolators feeding into two, feeding into one.
* A 2D cubic interpolater has four interpolators feeding into one.
* A 3D cubic interpolator has sixteen interpolators feeding into four, feeding into one.
To understand which values we need to look up, let's consider the 2D linear example again.
The four values going into the first group represent the four closest points (A, B, C, D) mentioned above.
1) The first interpolator gets:
* The closest value that is stored (A)
* The next value in the x dimension, keeping y fixed (B)
2) The second interpolator gets:
* One step over in the y dimension, keeping x fixed (C)
* One step over in both the x dimension and the y dimension (D)
The outputs of these two interpolators are points E and F.
In other words: the interpolated x values and, respectively, the following y values:
* The closest stored value of the y dimension
* One step forward in the y dimension
The last interpolator takes these two values and interpolates them in the y dimension.
To generalize for N dimensions and linear interpolation:
* The first group has 2^(n-1) parallel interpolators interpolating in the first dimension.
* The second group has 2^(n-2) parallel interpolators interpolating in the second dimension.
* The process continues until the n-th group, which has a single interpolator interpolating in the n-th dimension.
The same principle applies to the cubic interpolation in nD. The only difference is that there would be 4^(n-1) parallel interpolators in the first group, compared to 2^(n-1) for linear interpolation.
This is what the ``mixers`` function does.
Besides the values, each interpolator also needs to know the weight of each value in it's output.
Let's call this `d`, like in ``ba.interpolate``. It is the same for each group of interpolators, since it correlates to a dimension.
It's value is calculated the similarly to ``ba.interpolate``:
* First we prepare a "float table read-index" for that dimension (``id`` in ``ba.tabulate``)
* If the table only had that dimension and it could read a float index, what would it be.
* Then we ``int`` the float index to get the value we have stored that is closest to, but lower than the input value; the actual index for that dimension.
Our ``d`` is the difference between the float index and the actual index.
The ``ids`` function calculates the ``id`` for each dimension and inside the ``mixer`` function they get turned into ``d``s.
##### Storage method
The elephant in the room is: how do we get these indexes? For that we need to know how the values are stored.
We use one big table to store everything.
To understand the concept, let's look at the 2D example again, and then we'll extend it to 3d and the general nD case.
Let's say we have a 2D table with dimensions A and B where:
A has 3 values between 0 and 5 and B has 4 values between 0 and 1.
The 1D array representation of this 2D table will have a size of 3 * 4 = 12.
The values are stored in the following way:
* First 3 values: A is 0, then 3, then 5 while B is at 0.
* Next 3 values: A changes from 0 to 5 while B is at 1/3.
* Next 3 values: A changes from 0 to 5 while B is at 2/3.
* Last 3 values: A changes from 0 to 5 while B is at 1.
For the 3D example, let's extend the 2D example with an additional dimension C having 2 values between 0 and 2.
The total size will be 3 * 4 * 2 = 24.
The values are stored like so:
* First 3 values: A changes from 0 to 5, B is at 0, and C is at 0.
* Next 3 values: A changes from 0 to 5, B is at 1/3, and C is at 0.
* Next 3 values: A changes from 0 to 5, B is at 2/3, and C is at 0.
* Next 3 values: A changes from 0 to 5, B is at 1, and C is at 0.
The last 12 values are the same as the first 12, but with C at 2.
For the general n-dimensional case, we iterate through all dimensions, changing the values of the innermost dimension first, then moving towards the outer dimensions.
##### Read indexes
To get the float read index (``id``) corresponding to a particular dimension, we scale the function input value to be between 0 and 1, and multiply it by the size of that dimension minus one.
To understand how we get the ``readIndex``for ``.val``, let's work trough how we'd do it in our 2D linear example.
For simplicity's sake, the ranges of the inputs to our ``function`` are both 0 to 1.
Say we wanted to read the value closest to ``x=0.5`` and ``y=0``, so the ``id`` of ``x`` is ``1`` (the second value) and the ``id`` of ``y`` is 0 (first value). In this case, the read index is just the ``id`` of ``x``, rounded to the nearest integer, just like in ``ba.tabulate``.
If we want to read the value belonging to ``x=0.5`` and ``y=2/3``, things get more complicated. The ``id`` for ``y`` is now ``2``, the third value. For each step in the ``y`` direction, we need to increase the index by ``3``, the number of values that are stored for ``x``. So the influence of the ``y`` is:  the size of ``x`` times the rounded ``id`` of ``y``. The final read index is the rounded ``id`` of ``x`` plus the influence of ``y``.
For the general nD case, we need to do the same operation N times, each feeding into the next. This operation is the ``riN`` function. We take four parameters: the size of the dimension before it ``prevSize``, the index of the previous dimension ``prevIX``, the current size ``sizeX`` and the current id ``idX``.  ``riN`` has 2 outputs, the size, for feeding into the next dimension's ``prevSize``, and the read index feeding into the next dimension's ``prevIX``.
The size is the ``sizeX`` times ``prevSize``. The read index is the rounded ``idX`` times ``prevSize`` added to the ``prevIX``. Our final ``readIndex`` is the read index output of the last dimension.
To get the read values for the  interpolators need a pattern of offsets in each dimension, since we are looking for the read indexes surrounding the point of interest. These offsets are best explained by looking at the code of ``tabulate2d``, the hardcoded 2D version:
```faust
tabulate2d(C,function, sizeX,sizeY, rx0,ry0, rx1,ry1, x,y) =
environment {
size = sizeX*sizeY;
Maximum X index to access
midX = sizeX-1;
Maximum Y index to access
midY = sizeY-1;
Maximum total index to access
mid = size-1;
Create the table
wf = function(wfX,wfY);
Prepare the 'float' table read index for X
idX = (x-rx0)/(rx1-rx0)*midX;
Prepare the 'float' table read index for Y
idY = ((y-ry0)/(ry1-ry0))*midY;
table creation X:
wfX =
rx0+float(ba.time%sizeX)*(rx1-rx0)
float(midX);
table creation Y:
wfY =
ry0+
((float(ba.time-(ba.time%sizeX))
float(sizeX))
*(ry1-ry0))
float(midY);

Limit the table read index in [0, mid] if C = 1
rid(x,mid, 0) = x;
rid(x,mid, 1) = max(0, min(x, mid));

Tabulate a binary 'FX' function on a range [rx0, rx1] [ry0, ry1]
val(x,y) =
rdtable(size, wf, readIndex);
readIndex =
rid(
rid(int(idX+0.5),midX, C)
+yOffset
, mid, C);
yOffset = sizeX*rid(int(idY),midY,C);

Tabulate a binary 'FX' function over the range [rx0, rx1] [ry0, ry1] with linear interpolation
lin =
it.interpolate_linear(
dy
, it.interpolate_linear(dx,v0,v1)
, it.interpolate_linear(dx,v2,v3))
with {
i0 = rid(int(idX), midX, C)+yOffset;
i1 = i0+1;
i2 = i0+sizeX;
i3 = i1+sizeX;
dx  = idX-int(idX);
dy  = idY-int(idY);
v0 = rdtable(size, wf, rid(i0, mid, C));
v1 = rdtable(size, wf, rid(i1, mid, C));
v2 = rdtable(size, wf, rid(i2, mid, C));
v3 = rdtable(size, wf, rid(i3, mid, C));
};

Tabulate a binary 'FX' function over the range [rx0, rx1] [ry0, ry1] with cubic interpolation
cub =
it.interpolate_cubic(
dy
, it.interpolate_cubic(dx,v0,v1,v2,v3)
, it.interpolate_cubic(dx,v4,v5,v6,v7)
, it.interpolate_cubic(dx,v8,v9,v10,v11)
, it.interpolate_cubic(dx,v12,v13,v14,v15)
)
with {
i0  = i4-sizeX;
i1  = i5-sizeX;
i2  = i6-sizeX;
i3  = i7-sizeX;

i4  = i5-1;
i5  = rid(int(idX), midX, C)+yOffset;
i6  = i5+1;
i7  = i6+1;

i8  = i4+sizeX;
i9  = i5+sizeX;
i10 = i6+sizeX;
i11 = i7+sizeX;

i12 = i4+(2*sizeX);
i13 = i5+(2*sizeX);
i14 = i6+(2*sizeX);
i15 = i7+(2*sizeX);

dx  = idX-int(idX);
dy  = idY-int(idY);
v0  = rdtable(size, wf, rid(i0 , mid, C));
v1  = rdtable(size, wf, rid(i1 , mid, C));
v2  = rdtable(size, wf, rid(i2 , mid, C));
v3  = rdtable(size, wf, rid(i3 , mid, C));
v4  = rdtable(size, wf, rid(i4 , mid, C));
v5  = rdtable(size, wf, rid(i5 , mid, C));
v6  = rdtable(size, wf, rid(i6 , mid, C));
v7  = rdtable(size, wf, rid(i7 , mid, C));
v8  = rdtable(size, wf, rid(i8 , mid, C));
v9  = rdtable(size, wf, rid(i9 , mid, C));
v10 = rdtable(size, wf, rid(i10, mid, C));
v11 = rdtable(size, wf, rid(i11, mid, C));
v12 = rdtable(size, wf, rid(i12, mid, C));
v13 = rdtable(size, wf, rid(i13, mid, C));
v14 = rdtable(size, wf, rid(i14, mid, C));
v15 = rdtable(size, wf, rid(i15, mid, C));
};
};
```
In the interest of brevity, we'll stop explaining here. If you have any more questions, feel free to open an issue on [faustlibraries](https://github.com/grame-cncm/faustlibraries) and tag @magnetophon.
#### Test
```faust
ba = library("basics.lib");
powSin(x,y) = sin(pow(x,y));
tabulateNd_test = ba.tabulateNd(1, powSin, (8,8, 2.0,2.0, 8.0,8.0, 3.0,4.0)).lin;
```

---

## ba.if

-----------------------------`(ba.)if`-----------------------------------
if-then-else implemented with a select2. WARNING: since `select2` is strict (always evaluating both branches),
the resulting if does not have the usual "lazy" semantic of the C if form, and thus cannot be used to
protect against forbidden computations like division-by-zero for instance.
#### Usage
*   `if(cond, then, else) : _`
Where:
* `cond`: condition
* `then`: signal selected while cond is true
* `else`: signal selected while cond is false
#### Test
```faust
ba = library("basics.lib");
if_test = ba.if(1, 0.5, -0.5);
```

---

## ba.ifNc

-----------------------------`(ba.)ifNc`--------------------------------------
if-then-elseif-then-...elsif-then-else implemented on top of `ba.if`.
#### Usage
```faust
ifNc((cond1,then1, cond2,then2, ... condN,thenN, else)) : _
or
ifNc(Nc, cond1,then1, cond2,then2, ... condN,thenN, else) : _
or
cond1,then1, cond2,then2, ... condN,thenN, else : ifNc(Nc) : _
```
Where:
* `Nc` : number of branches/conditions (constant numerical expression)
* `condX`: condition
* `thenX`: signal selected if condX is the 1st true condition
* `else`: signal selected if all the cond1-condN conditions are false
#### Example test program
```faust
process(x,y) = ifNc((x<y,-1, x>y,+1, 0));
or
process(x,y) = ifNc(2, x<y,-1, x>y,+1, 0);
or
process(x,y) = x<y,-1, x>y,+1, 0 : ifNc(2);
```
outputs `-1` if `x<y`, `+1` if `x>y`, `0` otherwise.
#### Test
```faust
ba = library("basics.lib");
ifNc_test = ba.ifNc((1, 10, 0, 20, 30));
```

---

## ba.ifNcNo

-----------------------------`(ba.)ifNcNo`-------------------------------------
`ifNcNo(Nc,No)` is similar to `ifNc(Nc)` above but then/else branches have `No` outputs.
#### Usage
```faust
ifNcNo(Nc,No, cond1,then1, cond2,then2, ... condN,thenN, else) : sig.bus(No)
```
Where:
* `Nc` : number of branches/conditions (constant numerical expression)
* `No` : number of outputs (constant numerical expression)
* `condX`: condition
* `thenX`: list of No signals selected if condX is the 1st true condition
* `else`: list of No signals selected if all the cond1-condN conditions are false
#### Example test program
```faust
process(x) = ifNcNo(2,3, x<0, -1,-1,-1, x>0, 1,1,1, 0,0,0);
```
outputs `-1,-1,-1` if `x<0`, `1,1,1` if `x>0`, `0,0,0` otherwise.
#### Test
```faust
ba = library("basics.lib");
ifNcNo_test = (1, 10, 0, 20, 30) : ba.ifNcNo(2, 1);
```

---

## ba.selector

-----------------------------`(ba.)selector`---------------------------------
Selects the ith input among n at compile time.
#### Usage
```faust
selector(I,N)
_,_,_,_ : selector(2,4) : _ // selects the 3rd input among 4
```
Where:
* `I`: input to select (int, numbered from 0, known at compile time)
* `N`: number of inputs (int, known at compile time, N > I)
There is also `cselector` for selecting among complex input signals of the form (real,imag).
#### Test
```faust
ba = library("basics.lib");
selector_test = (0.1, 0.2, 0.3, 0.4) : ba.selector(2, 4);
```

---

## ba.select2stereo

--------------------`(ba.)select2stereo`--------------------
Select between 2 stereo signals.
#### Usage
```faust
_,_,_,_ : select2stereo(bpc) : _,_
```
Where:
* `bpc`: the selector switch (0/1)
#### Test
```faust
ba = library("basics.lib");
select2stereo_test = ba.select2stereo(1, (0.1,0.2, 0.3,0.4));
```

---

## ba.selectn

-----------------------------`(ba.)selectn`---------------------------------
Selects the ith input among N at run time.
#### Usage
```faust
selectn(N,i)
_,_,_,_ : selectn(4,2) : _ // selects the 3rd input among 4
```
Where:
* `N`: number of inputs (int, known at compile time, N > 0)
* `i`: input to select (int, numbered from 0)
#### Example test program
```faust
N = 64;
process = par(n, N, (par(i,N,i) : selectn(N,n)));
```
#### Test
```faust
ba = library("basics.lib");
selectn_test = (1,2,3,4) : ba.selectn(4, 2);
```

---

## ba.selectbus

----------------------`(ba.)selectbus`-----------------------------------------
Select a bus among `NUM_BUSES` buses, where each bus has `BUS_SIZE` outputs.
The order of the signal inputs should be the signals of the first bus, the
signals of the second bus, and so on.
#### Usage
```faust
process = si.bus(BUS_SIZE*NUM_BUSES) : selectbus(BUS_SIZE, NUM_BUSES, id) : si.bus(BUS_SIZE);
```
Where:
* `BUS_SIZE`: number of outputs from each bus (int, known at compile time).
* `NUM_BUSES`: number of buses (int, known at compile time).
* `id`: index of the bus to select (int, `0<=id<NUM_BUSES`)
#### Test
```faust
ba = library("basics.lib");
selectbus_test = (1,2,3,4) : ba.selectbus(2, 2, 1);
```

---

## ba.selectxbus

----------------------`(ba.)selectxbus`-----------------------------------------
Like `ba.selectbus`, but with a cross-fade when selecting the bus using the same
technique than `ba.selectmulti`.
#### Usage
```faust
process = si.bus(BUS_SIZE*NUM_BUSES) : selectbus(BUS_SIZE, NUM_BUSES, FADE, id) : si.bus(BUS_SIZE);
```
Where:
* `BUS_SIZE`: number of outputs from each bus (int, known at compile time).
* `NUM_BUSES`: number of buses (int, known at compile time).
* `fade`: number of samples for the crossfade.
* `id`: index of the bus to select (int, `0<=id<NUM_BUSES`)
#### Test
```faust
ba = library("basics.lib");
selectxbus_test = (1,2,3,4) : ba.selectxbus(2, 2, 16, checkbox("bus"));
```

---

## ba.selectmulti

-----------------------------`(ba.)selectmulti`---------------------------------
Selects the ith circuit among N at run time (all should have the same number of inputs and outputs)
with a crossfade.
#### Usage
```faust
selectmulti(n,lgen,id)
```
Where:
* `n`: crossfade in samples
* `lgen`: list of circuits
* `id`: circuit to select (int, numbered from 0)
#### Example test program
```faust
process = selectmulti(ma.SR/10, ((3,9),(2,8),(5,7)), nentry("choice", 0, 0, 2, 1));
process = selectmulti(ma.SR/10, ((_*3,_*9),(_*2,_*8),(_*5,_*7)), nentry("choice", 0, 0, 2, 1));
```
#### Test
```faust
ba = library("basics.lib");
os = library("oscillators.lib");
ma = library("maths.lib");
effects = ((_*0.5,_*0.5),(_*0.25,_*0.25));
choice = int(checkbox("choice"));
selectmulti_test = (os.osc(440), os.osc(660)) : ba.selectmulti(ma.SR/100, effects, choice);
```

---

## ba.selectoutn

-----------------------------`(ba.)selectoutn`---------------------------------
Route input to the output among N at run time.
#### Usage
```faust
_ : selectoutn(N, i) : si.bus(N)
```
Where:
* `N`: number of outputs (int, known at compile time, N > 0)
* `i`: output number to route to (int, numbered from 0) (i.e. slider)
#### Example test program
```faust
process = 1 : selectoutn(3, sel) : par(i, 3, vbargraph("v.bargraph %i", 0, 1));
sel = hslider("volume", 0, 0, 2, 1) : int;
```
#### Test
```faust
ba = library("basics.lib");
selectoutn_test = 1 : ba.selectoutn(3, 1);
```

---

## ba.latch

----------------------------`(ba.)latch`--------------------------------
Latch input on the rising edge of trig.
Captures ("records") the input x whenever trig crosses from ≤0 to >0,
and holds the last captured value at all other times.
#### Usage
```faust
_ : latch(trig) : _
```
Where:
* `trig`: trigger signal. A rising edge (≤0 → >0) samples the input.
#### Test
```faust
ba = library("basics.lib");
os = library("oscillators.lib");
latch_test = os.osc(2) : ba.latch(button("hold"));
```

---

## ba.sAndH

--------------------------`(ba.)sAndH`-------------------------------
Sample And Hold: "records" the input when trig is 1, outputs a frozen value when trig is 0.
`sAndH` is a standard Faust function.
#### Usage
```faust
_ : sAndH(trig) : _
```
Where:
* `trig`: hold trigger (0 for hold, 1 for bypass)
#### Test
```faust
ba = library("basics.lib");
os = library("oscillators.lib");
sAndH_test = os.osc(2) : ba.sAndH(button("hold"));
```

---

## ba.tAndH

--------------------------`(ba.)tAndH`-------------------------------
Test And Hold: "records" the input when pred(input) is true, outputs a frozen value otherwise.
#### Usage
```faust
_ : tAndH(pred) : _
```
Where:
* `pred`: predicate to test the input
#### Test
```faust
ba = library("basics.lib");
os = library("oscillators.lib");
isPositive(x) = x > 0.0;
tAndH_test = os.osc(2) : ba.tAndH(isPositive);
```

---

## ba.downSample

--------------------------`(ba.)downSample`-------------------------------
Down sample a signal. WARNING: this function doesn't change the
rate of a signal, it just holds samples...
`downSample` is a standard Faust function.
#### Usage
```faust
_ : downSample(freq) : _
```
Where:
* `freq`: new rate in Hz
#### Test
```faust
ba = library("basics.lib");
os = library("oscillators.lib");
downSample_test = os.osc(440) : ba.downSample(11025);
```

---

## ba.downSampleCV

--------------------------`(ba.)downSampleCV`---------------------------
A version of `ba.downSample` where the frequency parameter has
been replaced by an `amount` parameter that is in the range zero
to one. WARNING: this function doesn't change the rate of a
signal, it just holds samples...
#### Usage
```faust
_ : downSampleCV(amount) : _
```
Where:
* `amount`: The amount of down-sampling to perform [0..1]
#### Test
```faust
ba = library("basics.lib");
os = library("oscillators.lib");
downSampleCV_test = os.osc(440) : ba.downSampleCV(0.5);
```

---

## ba.peakhold

------------------`(ba.)peakhold`---------------------------
Outputs current max value above zero.
#### Usage
```faust
_ : peakhold(mode) : _
```
Where:
`mode` means:
0 - Pass through. A single sample 0 trigger will work as a reset.
1 - Track and hold max value.
#### Test
```faust
ba = library("basics.lib");
os = library("oscillators.lib");
peakhold_test = os.osc(440) : ba.peakhold(1);
```

---

## ba.peakholder

------------------`(ba.)peakholder`-------------------------------------------
While peak-holder functions are scarcely discussed in the literature
(please do send me an email if you know otherwise), common sense
tells that the expected behaviour should be as follows: the absolute
value of the input signal is compared with the output of the peak-holder;
if the input is greater or equal to the output, a new peak is detected
and sent to the output; otherwise, a timer starts and the current peak
is held for N samples; once the timer is out and no new peaks have been
detected, the absolute value of the current input becomes the new peak.
#### Usage
```faust
_ : peakholder(holdTime) : _
```
Where:
* `holdTime`: hold time in samples
#### Test
```faust
ba = library("basics.lib");
os = library("oscillators.lib");
peakholder_test = os.osc(440) : ba.peakholder(ba.sec2samp(0.1));
```

---

## ba.kr2ar

--------------------------`(ba.)kr2ar`---------------------------
Force a control rate signal to be used as an audio rate signal.
#### Usage
```faust
hslider("freq", 200, 200, 2000, 0.1) : kr2ar;
```
#### Test
```faust
ba = library("basics.lib");
kr2ar_test = button("gate") : ba.kr2ar;
```

---

## ba.impulsify

--------------------------`(ba.)impulsify`---------------------------
Turns a signal into an impulse with the value of the current sample
(0.3,0.2,0.1 becomes 0.3,0.0,0.0). This function is typically used with a
`button` to turn its output into an impulse. `impulsify` is a standard Faust
function.
#### Usage
```faust
button("gate") : impulsify;
```
#### Test
```faust
ba = library("basics.lib");
os = library("oscillators.lib");
impulsify_test = os.osc(440) : ba.impulsify;
```

---

## ba.automat

-----------------------`(ba.)automat`------------------------------
Record and replay in a loop the successives values of the input signal.
#### Usage
```faust
hslider(...) : automat(t, size, init) : _
```
Where:
* `t`: tempo in BPM
* `size`: number of items in the loop
* `init`: init value in the loop
#### Test
```faust
ba = library("basics.lib");
autoControl = hslider("autoControl", 0.2, 0, 1, 0.01);
automat_test = autoControl : ba.automat(120, 4, 0.0);
```

---

## ba.bpf

-----------------`(ba.)bpf`-------------------
bpf is an environment (a group of related definitions) that can be used to
create break-point functions. It contains three functions:
* `start(x,y)` to start a break-point function
* `end(x,y)` to end a break-point function
* `point(x,y)` to add intermediate points to a break-point function, using linear interpolation
A minimal break-point function must contain at least a start and an end point:
```faust
f = bpf.start(x0,y0) : bpf.end(x1,y1);
```
A more involved break-point function can contains any number of intermediate
points:
```faust
f = bpf.start(x0,y0) : bpf.point(x1,y1) : bpf.point(x2,y2) : bpf.end(x3,y3);
```
In any case the `x_{i}` must be in increasing order (for all `i`, `x_{i} < x_{i+1}`).
For example the following definition:
```faust
f = bpf.start(x0,y0) : ... : bpf.point(xi,yi) : ... : bpf.end(xn,yn);
```
implements a break-point function f such that:
* `f(x) = y_{0}` when `x < x_{0}`
* `f(x) = y_{n}` when `x > x_{n}`
* `f(x) = y_{i} + (y_{i+1}-y_{i})*(x-x_{i})/(x_{i+1}-x_{i})` when `x_{i} <= x`
and `x < x_{i+1}`
In addition to `bpf.point`, there are also `step` and `curve` functions:
* `step(x,y)` to add a flat section
* `step_end(x,y)` to end with a flat section
* `curve(B,x,y)` to add a curved section
* `curve_end(B,x,y)` to end with a curved section
These functions can be combined with the other `bpf` functions.
Here's an example using `bpf.step`:
`f(x) = x : bpf.start(0,0) : bpf.step(.2,.3) : bpf.step(.4,.6) : bpf.step_end(1,1);`
For `x < 0.0`, the output is 0.0.
For `0.0 <= x < 0.2`, the output is 0.0.
For `0.2 <= x < 0.4`, the output is 0.3.
For `0.4 <= x < 1.0`, the output is 0.6.
For `1.0 <= x`, the output is 1.0
For the `curve` functions, `B` (compile-time constant)
is a "bias" value strictly greater than zero and less than or equal to 1. When `B` is 0.5, the
output curve is exactly linear and equivalent to `bpf.point`. When `B` is less than 0.5, the
output is biased towards the `y` value of the previous breakpoint. When `B` is greater than 0.5,
the output is biased towards the `y` value of the curve breakpoint. Here's an example:
`f = bpf.start(0,0) : bpf.curve(.15,.5,.5) : bpf.curve_end(.85,1,1);`
In the following example, the output is biased towards zero (the latter y value) instead of
being a linear ramp from 1 to 0.
`f = bpf.start(0,1) : bpf.curve_end(.9,1,0);`
`bpf` is a standard Faust function.

---

## ba.listInterp

-------------------`(ba.)listInterp`-------------------------
Linearly interpolates between the elements of a list.
#### Usage
```faust
index = 1.69; // range is 0-4
process = listInterp((800,400,350,450,325),index);
```
Where:
* `index`: the index (float) to interpolate between the different values.
The range of `index` depends on the size of the list.
#### Test
```faust
ba = library("basics.lib");
listInterp_test = ba.listInterp((800,400,350,450,325), 1.5);
```

---

## ba.bypass1

-------------------`(ba.)bypass1`-------------------------
Takes a mono input signal, route it to `e` and bypass it if `bpc = 1`.
When bypassed, `e` is feed with zeros so that its state is cleanup up.
`bypass1` is a standard Faust function.
#### Usage
```faust
_ : bypass1(bpc,e) : _
```
Where:
* `bpc`: bypass switch (0/1)
* `e`: a mono effect
#### Test
```faust
ba = library("basics.lib");
os = library("oscillators.lib");
bypass1_test = os.osc(440) : ba.bypass1(button("bypass"), *(0.5));
```
License: STK-4.3

---

## ba.bypass2

-------------------`(ba.)bypass2`-------------------------
Takes a stereo input signal, route it to `e` and bypass it if `bpc = 1`.
When bypassed, `e` is feed with zeros so that its state is cleanup up.
`bypass2` is a standard Faust function.
#### Usage
```faust
_,_ : bypass2(bpc,e) : _,_
```
Where:
* `bpc`: bypass switch (0/1)
* `e`: a stereo effect
#### Test
```faust
ba = library("basics.lib");
os = library("oscillators.lib");
bypass2_test = (os.osc(440), os.osc(660)) : ba.bypass2(button("bypass"), par(i,2, *(0.5)));
```
License: STK-4.3

---

## ba.bypass1to2

-------------------`(ba.)bypass1to2`-------------------------
Bypass switch for effect `e` having mono input signal and stereo output.
Effect `e` is bypassed if `bpc = 1`.When bypassed, `e` is feed with zeros
so that its state is cleanup up.
`bypass1to2` is a standard Faust function.
#### Usage
```faust
_ : bypass1to2(bpc,e) : _,_
```
Where:
* `bpc`: bypass switch (0/1)
* `e`: a mono-to-stereo effect
#### Test
```faust
ba = library("basics.lib");
os = library("oscillators.lib");
monoToStereo(x) = (x*0.5, x*0.25);
bypass1to2_test = os.osc(440) : ba.bypass1to2(button("bypass"), monoToStereo);
```
License: STK-4.3

---

## ba.bypass_fade

-------------------`(ba.)bypass_fade`-------------------------
Bypass an arbitrary (N x N) circuit with 'n' samples crossfade.
Inputs and outputs signals are faded out when 'e' is bypassed,
so that 'e' state is cleanup up.
Once bypassed the effect is replaced by `par(i,N,_)`.
Bypassed circuits can be chained.
#### Usage
```faust
_ : bypass_fade(n,b,e) : _
or
_,_ : bypass_fade(n,b,e) : _,_
```
* `n`: number of samples for the crossfade
* `b`: bypass switch (0/1)
* `e`: N x N circuit
#### Example test program
```faust
process = bypass_fade(ma.SR/10, checkbox("bypass echo"), echo);
process = bypass_fade(ma.SR/10, checkbox("bypass reverb"), freeverb);
```
#### Test
```faust
ba = library("basics.lib");
os = library("oscillators.lib");
bypass_fade_test = (os.osc(440), os.osc(660)) : ba.bypass_fade(128, button("bypass"), par(i,2, *(0.5)));
```

---

## ba.toggle

----------------------------`(ba.)toggle`------------------------------------------
Triggered by the change of 0 to 1, it toggles the output value
between 0 and 1.
#### Usage
```faust
_ : toggle : _
```
#### Example test program
```faust
button("toggle") : toggle : vbargraph("output", 0, 1)
(an.amp_follower(0.1) > 0.01) : toggle : vbargraph("output", 0, 1) // takes audio input
```
#### Test
```faust
ba = library("basics.lib");
toggle_test = ba.toggle(button("trig"));
```

---

## ba.on_and_off

----------------------------`(ba.)on_and_off`------------------------------------------
The first channel set the output to 1, the second channel to 0.
#### Usage
```faust
_,_ : on_and_off : _
```
#### Example test program
```faust
button("on"), button("off") : on_and_off : vbargraph("output", 0, 1)
```
#### Test
```faust
ba = library("basics.lib");
on_and_off_test = button("on"), button("off") : ba.on_and_off;
```

---

## ba.bitcrusher

----------------------------`(ba.)bitcrusher`------------------------------------------
Produce distortion by reduction of the signal resolution.
#### Usage
```faust
_ : bitcrusher(nbits) : _
```
Where:
* `nbits`: the number of bits of the wanted resolution
#### Test
```faust
ba = library("basics.lib");
os = library("oscillators.lib");
bitcrusher_test = os.osc(440) : ba.bitcrusher(8);
```

---

## ba.mulaw_bitcrusher

----------------------------`(ba.)mulaw_bitcrusher`------------------------------------------
Produce distortion by reducing the signal resolution using μ-law compression.
#### Usage
```faust
_ : mulaw_bitcrusher(mu,nbits) : _
```
Where:
* `mu`: controls the degree of μ-law compression, larger values result in stronger compression
* `nbits`: the number of bits of the wanted resolution
#### Description
The `mulaw_bitcrusher` applies a combination of μ-law compression, quantization, and expansion
to create a non-linear bitcrushed effect. This method retains finer detail in lower-amplitude signals
compared to linear bitcrushing, making it suitable for creative sound design.
#### Theory
1. **μ-law Compression**:
emphasizes lower-amplitude signals by applying a logarithmic curve to the signal.
The formula used is:
```faust
F(x) = ma.signum(x) * log(1 + mu * abs(x)) / log(1 + mu);
```
2. **Quantization**:
reduces the signal resolution to `nbits` by rounding values to the nearest step within the specified bit depth.
3. **μ-law Expansion**:
reverses the compression applied earlier to restore the signal to its original dynamic range:
```faust
F⁻¹(y) = ma.signum(y) * (pow(1 + mu, abs(y)) - 1) / mu;
```
#### Example test program
```faust
process = os.osc(440) : mulaw_bitcrusher(255, 8);
```
In this example, a sine wave at 440 Hz is passed through the μ-law bitcrusher, with a compression
parameter `mu` of 255 and 8-bit quantization. This creates a distorted, "lo-fi" effect.
#### Test
```faust
ba = library("basics.lib");
os = library("oscillators.lib");
mulaw_bitcrusher_test = os.osc(440) : ba.mulaw_bitcrusher(2.0, 8);
```
#### References
* <https://en.wikipedia.org/wiki/Μ-law_algorithm>

---

## ba.slidingReduce

-----------------------------`(ba.)slidingReduce`-----------------------------
Fold-like high order function. Apply a commutative binary operation `op` to
the last `n` consecutive samples of a signal `x`. For example :
`slidingReduce(max,128,128,0-(ma.MAX))` will compute the maximum of the last
128 samples. The output is updated each sample, unlike reduce, where the
output is constant for the duration of a block.
#### Usage
```faust
_ : slidingReduce(op,n,maxN,disabledVal) : _
```
Where:
* `n`: the number of values to process
* `maxN`: the maximum number of values to process (int, known at compile time, maxN > 0)
* `op`: the operator. Needs to be a commutative one.
* `disabledVal`: the value to use when we want to ignore a value.
In other words, `op(x,disabledVal)` should equal to `x`. For example,
`+(x,0)` equals `x` and `min(x,ma.MAX)` equals `x`. So if we want to
calculate the sum, we need to give 0 as `disabledVal`, and if we want the
minimum, we need to give `ma.MAX` as `disabledVal`.
#### Test
```faust
ba = library("basics.lib");
os = library("oscillators.lib");
ma = library("maths.lib");
slidingReduce_test = os.osc(440) : ba.slidingReduce(max, 64, 64, 0 - ma.MAX);
```

---

## ba.slidingSum

------------------------------`(ba.)slidingSum`------------------------------
The sliding sum of the last n input samples.
It will eventually run into numerical trouble when there is a persistent dc component.
If that matters in your application, use the more CPU-intensive `ba.slidingSump`.
#### Usage
```faust
_ : slidingSum(n) : _
```
Where:
* `n`: the number of values to process
#### Test
```faust
ba = library("basics.lib");
os = library("oscillators.lib");
slidingSum_test = os.osc(440) : ba.slidingSum(64);
```

---

## ba.slidingSump

------------------------------`(ba.)slidingSump`------------------------------
The sliding sum of the last n input samples.
It uses a lot more CPU than `ba.slidingSum`, but is numerically stable "forever" in return.
#### Usage
```faust
_ : slidingSump(n,maxN) : _
```
Where:
* `n`: the number of values to process
* `maxN`: the maximum number of values to process (int, known at compile time, maxN > 0)
#### Test
```faust
ba = library("basics.lib");
os = library("oscillators.lib");
slidingSump_test = os.osc(440) : ba.slidingSump(64, 128);
```

---

## ba.slidingMax

----------------------------`(ba.)slidingMax`--------------------------------
The sliding maximum of the last n input samples.
#### Usage
```faust
_ : slidingMax(n,maxN) : _
```
Where:
* `n`: the number of values to process
* `maxN`: the maximum number of values to process (int, known at compile time, maxN > 0)
#### Test
```faust
ba = library("basics.lib");
os = library("oscillators.lib");
ma = library("maths.lib");
slidingMax_test = os.osc(440) : ba.slidingMax(64, 128);
```

---

## ba.slidingMin

----------------------------`(ba.)slidingMin`--------------------------------
The sliding minimum of the last n input samples.
#### Usage
```faust
_ : slidingMin(n,maxN) : _
```
Where:
* `n`: the number of values to process
* `maxN`: the maximum number of values to process (int, known at compile time, maxN > 0)
#### Test
```faust
ba = library("basics.lib");
os = library("oscillators.lib");
ma = library("maths.lib");
slidingMin_test = os.osc(440) : ba.slidingMin(64, 128);
```

---

## ba.slidingMean

----------------------------`(ba.)slidingMean`-------------------------------
The sliding mean of the last n input samples.
It will eventually run into numerical trouble when there is a persistent dc component.
If that matters in your application, use the more CPU-intensive `ba.slidingMeanp`.
#### Usage
```faust
_ : slidingMean(n) : _
```
Where:
* `n`: the number of values to process
#### Test
```faust
ba = library("basics.lib");
os = library("oscillators.lib");
slidingMean_test = os.osc(440) : ba.slidingMean(64);
```

---

## ba.slidingMeanp

----------------------------`(ba.)slidingMeanp`-------------------------------
The sliding mean of the last n input samples.
It uses a lot more CPU than `ba.slidingMean`, but is numerically stable "forever" in return.
#### Usage
```faust
_ : slidingMeanp(n,maxN) : _
```
Where:
* `n`: the number of values to process
* `maxN`: the maximum number of values to process (int, known at compile time, maxN > 0)
#### Test
```faust
ba = library("basics.lib");
os = library("oscillators.lib");
slidingMeanp_test = os.osc(440) : ba.slidingMeanp(64, 128);
```

---

## ba.slidingRMS

---------------------------`(ba.)slidingRMS`---------------------------------
The root mean square of the last n input samples.
It will eventually run into numerical trouble when there is a persistent dc component.
If that matters in your application, use the more CPU-intensive `ba.slidingRMSp`.
#### Usage
```faust
_ : slidingRMS(n) : _
```
Where:
* `n`: the number of values to process
#### Test
```faust
ba = library("basics.lib");
os = library("oscillators.lib");
slidingRMS_test = os.osc(440) : ba.slidingRMS(64);
```

---

## ba.slidingRMSp

---------------------------`(ba.)slidingRMSp`---------------------------------
The root mean square of the last n input samples.
It uses a lot more CPU than `ba.slidingRMS`, but is numerically stable "forever" in return.
#### Usage
```faust
_ : slidingRMSp(n,maxN) : _
```
Where:
* `n`: the number of values to process
* `maxN`: the maximum number of values to process (int, known at compile time, maxN > 0)
#### Test
```faust
ba = library("basics.lib");
os = library("oscillators.lib");
slidingRMSp_test = os.osc(440) : ba.slidingRMSp(64, 128);
```

---

## ba.parallelOp

-----------------------------`(ba.)parallelOp`-----------------------------
Apply a commutative binary operation `op` to N parallel inputs.
#### usage
```faust
si.bus(N) : parallelOp(op,N) : _
```
where:
* `N`: the number of parallel inputs known at compile time
* `op`: the operator which needs to be commutative
#### Test
```faust
ba = library("basics.lib");
parallelOp_test = (0.2, 0.5, 0.1) : ba.parallelOp(max, 3);
```

---

## ba.parallelMax

---------------------------`(ba.)parallelMax`---------------------------------
The maximum of N parallel inputs.
#### Usage
```faust
si.bus(N) : parallelMax(N) : _
```
Where:
* `N`: the number of parallel inputs known at compile time
#### Test
```faust
ba = library("basics.lib");
parallelMax_test = (0.2, 0.5, 0.1) : ba.parallelMax(3);
```

---

## ba.parallelMin

---------------------------`(ba.)parallelMin`---------------------------------
The minimum of N parallel inputs.
#### Usage
```faust
si.bus(N) : parallelMin(N) : _
```
Where:
* `N`: the number of parallel inputs known at compile time
#### Test
```faust
ba = library("basics.lib");
parallelMin_test = (0.2, 0.5, 0.1) : ba.parallelMin(3);
```

---

## ba.parallelMean

---------------------------`(ba.)parallelMean`---------------------------------
The mean of N parallel inputs.
#### Usage
```faust
si.bus(N) : parallelMean(N) : _
```
Where:
* `N`: the number of parallel inputs known at compile time
#### Test
```faust
ba = library("basics.lib");
parallelMean_test = (0.2, 0.5, 0.1) : ba.parallelMean(3);
```

---

## ba.parallelRMS

---------------------------`(ba.)parallelRMS`---------------------------------
The RMS of N parallel inputs.
#### Usage
```faust
si.bus(N) : parallelRMS(N) : _
```
Where:
* `N`: the number of parallel inputs known at compile time
#### Test
```faust
ba = library("basics.lib");
parallelRMS_test = (0.2, 0.5, 0.1) : ba.parallelRMS(3);
```

---

# compressors.lib
**Prefix:** `co`

################################ compressors.lib ##########################################
Compressors library. Its official prefix is `co`.

This library provides building blocks and complete dynamic processors
including compressors, limiters, expanders, and gates.

The Compressors library is organized into 6 sections:

* [Conversion Tools](#conversion-tools)
* [Functions Reference](#functions-reference)
* [Linear gain computer section](#linear-gain-computer-section)
* [Original versions section](#original-versions-section)
* [Expanders](#expanders)
* [Lookahead Limiters](#lookahead-limiters)

#### References

* <https://github.com/grame-cncm/faustlibraries/blob/master/compressors.lib>
########################################################################################

## co.peak_compression_gain_mono_db

--------------------`(co.)peak_compression_gain_mono_db`-------------------
Mono dynamic range compressor gain computer with dB output.
`peak_compression_gain_mono_db` is a standard Faust function.
#### Usage
```faust
_ : peak_compression_gain_mono_db(strength,thresh,att,rel,knee,prePost) : _
```
Where:
* `strength`: strength of the compression (0 = no compression, 1 means hard limiting, >1 means over-compression)
* `thresh`: dB level threshold above which compression kicks in
* `att`: attack time = time constant (sec) when level & compression going up
* `rel`: release time = time constant (sec) coming out of compression
* `knee`: a gradual increase in gain reduction around the threshold:
below thresh-(knee/2) there is no gain reduction,
above thresh+(knee/2) there is the same gain reduction as without a knee,
and in between there is a gradual increase in gain reduction
* `prePost`: places the level detector either at the input or after the gain computer;
this turns it from a linear return-to-zero detector into a log domain return-to-threshold detector
It uses a strength parameter instead of the traditional ratio, in order to be able to
function as a hard limiter.
For that you'd need a ratio of infinity:1, and you cannot express that in Faust.
Sometimes even bigger ratios are useful:
for example a group recording where one instrument is recorded with both a close microphone and a room microphone,
and the instrument is loud enough in the room mic when playing loud, but you want to boost it when it is playing soft.
#### Test
```faust
co = library("compressors.lib");
os = library("oscillators.lib");
peak_compression_gain_mono_db_test = os.osc(440) : co.peak_compression_gain_mono_db(0.5, -12, 0.01, 0.1, 6, 0);
```
#### References
* <http://en.wikipedia.org/wiki/Dynamic_range_compression>
* Digital Dynamic Range Compressor Design: A Tutorial and Analysis, Dimitrios GIANNOULIS (<Dimitrios.Giannoulis@eecs.qmul.ac.uk>), Michael MASSBERG (<michael@massberg.org>), and Josuah D.REISS (<josh.reiss@eecs.qmul.ac.uk>)

---

## co.peak_compression_gain_N_chan_db

--------------------`(co.)peak_compression_gain_N_chan_db`-------------------
N channels dynamic range compressor gain computer with dB output.
`peak_compression_gain_N_chan_db` is a standard Faust function.
#### Usage
```faust
si.bus(N) : peak_compression_gain_N_chan_db(strength,thresh,att,rel,knee,prePost,link,N) : si.bus(N)
```
Where:
* `strength`: strength of the compression (0 = no compression, 1 means hard limiting, >1 means over-compression)
* `thresh`: dB level threshold above which compression kicks in
* `att`: attack time = time constant (sec) when level & compression going up
* `rel`: release time = time constant (sec) coming out of compression
* `knee`: a gradual increase in gain reduction around the threshold:
below thresh-(knee/2) there is no gain reduction,
above thresh+(knee/2) there is the same gain reduction as without a knee,
and in between there is a gradual increase in gain reduction
* `prePost`: places the level detector either at the input or after the gain computer;
this turns it from a linear return-to-zero detector into a log  domain return-to-threshold detector
* `link`: the amount of linkage between the channels: 0 = each channel is independent, 1 = all channels have the same amount of gain reduction
* `N`: the number of channels of the compressor, known at compile time
It uses a strength parameter instead of the traditional ratio, in order to be able to
function as a hard limiter.
For that you'd need a ratio of infinity:1, and you cannot express that in Faust.
Sometimes even bigger ratios are useful:
for example a group recording where one instrument is recorded with both a close microphone and a room microphone,
and the instrument is loud enough in the room mic when playing loud, but you want to boost it when it is playing soft.
#### Test
```faust
co = library("compressors.lib");
os = library("oscillators.lib");
peak_compression_gain_N_chan_db_test = (os.osc(440), os.osc(660)) : co.peak_compression_gain_N_chan_db(0.5, -12, 0.01, 0.1, 6, 0, 0.5, 2);
```
#### References
* <http://en.wikipedia.org/wiki/Dynamic_range_compression>
* Digital Dynamic Range Compressor Design: A Tutorial and Analysis, Dimitrios GIANNOULIS (<Dimitrios.Giannoulis@eecs.qmul.ac.uk>), Michael MASSBERG (<michael@massberg.org>), and Josuah D.REISS (<josh.reiss@eecs.qmul.ac.uk>)
generalise compression gains for N channels.
first we define a mono version:

---

## co.FFcompressor_N_chan

--------------------`(co.)FFcompressor_N_chan`-------------------
Feed forward N channels dynamic range compressor.
`FFcompressor_N_chan` is a standard Faust function.
#### Usage
```faust
si.bus(N) : FFcompressor_N_chan(strength,thresh,att,rel,knee,prePost,link,meter,N) : si.bus(N)
```
Where:
* `strength`: strength of the compression (0 = no compression, 1 means hard limiting, >1 means over-compression)
* `thresh`: dB level threshold above which compression kicks in
* `att`: attack time = time constant (sec) when level & compression going up
* `rel`: release time = time constant (sec) coming out of compression
* `knee`: a gradual increase in gain reduction around the threshold:
below thresh-(knee/2) there is no gain reduction,
above thresh+(knee/2) there is the same gain reduction as without a knee,
and in between there is a gradual increase in gain reduction
* `prePost`: places the level detector either at the input or after the gain computer;
this turns it from a linear return-to-zero detector into a log  domain return-to-threshold detector
* `link`: the amount of linkage between the channels: 0 = each channel is independent, 1 = all channels have the same amount of gain reduction
* `meter`: a gain reduction meter. It can be implemented like so:
`meter = _<:(_, (ba.linear2db:max(maxGR):meter_group((hbargraph("[1][unit:dB][tooltip: gain reduction in dB]", maxGR, 0))))):attach;`
* `N`: the number of channels of the compressor, known at compile time
It uses a strength parameter instead of the traditional ratio, in order to be able to
function as a hard limiter.
For that you'd need a ratio of infinity:1, and you cannot express that in Faust.
Sometimes even bigger ratios are useful:
for example a group recording where one instrument is recorded with both a close microphone and a room microphone,
and the instrument is loud enough in the room mic when playing loud, but you want to boost it when it is playing soft.
#### Test
```faust
co = library("compressors.lib");
os = library("oscillators.lib");
meter(x) = x;
FFcompressor_N_chan_test = (os.osc(440), os.osc(660)) : co.FFcompressor_N_chan(0.5, -12, 0.01, 0.1, 6, 0, 0.5, meter, 2);
```
#### References
* <http://en.wikipedia.org/wiki/Dynamic_range_compression>
* Digital Dynamic Range Compressor Design: A Tutorial and Analysis, Dimitrios GIANNOULIS (<Dimitrios.Giannoulis@eecs.qmul.ac.uk>), Michael MASSBERG (<michael@massberg.org>), and Josuah D.REISS (<josh.reiss@eecs.qmul.ac.uk>)
feed forward compressor

---

## co.FBcompressor_N_chan

--------------------`(co.)FBcompressor_N_chan`-------------------
Feed back N channels dynamic range compressor.
`FBcompressor_N_chan` is a standard Faust function.
#### Usage
```faust
si.bus(N) : FBcompressor_N_chan(strength,thresh,att,rel,knee,prePost,link,meter,N) : si.bus(N)
```
Where:
* `strength`: strength of the compression (0 = no compression, 1 means hard limiting, >1 means over-compression)
* `thresh`: dB level threshold above which compression kicks in
* `att`: attack time = time constant (sec) when level & compression going up
* `rel`: release time = time constant (sec) coming out of compression
* `knee`: a gradual increase in gain reduction around the threshold:
below thresh-(knee/2) there is no gain reduction,
above thresh+(knee/2) there is the same gain reduction as without a knee,
and in between there is a gradual increase in gain reduction
* `prePost`: places the level detector either at the input or after the gain computer;
this turns it from a linear return-to-zero detector into a log  domain return-to-threshold detector
* `link`: the amount of linkage between the channels. 0 = each channel is independent, 1 = all channels have the same amount of gain reduction
* `meter`: a gain reduction meter. It can be implemented with:
`meter = _ <: (_,(ba.linear2db:max(maxGR):meter_group((hbargraph("[1][unit:dB][tooltip: gain reduction in dB]", maxGR, 0))))):attach;`
or it can be omitted by defining `meter = _;`.
* `N`: the number of channels of the compressor, known at compile time
It uses a strength parameter instead of the traditional ratio, in order to be able to
function as a hard limiter.
For that you'd need a ratio of infinity:1, and you cannot express that in Faust.
Sometimes even bigger ratios are useful:
for example a group recording where one instrument is recorded with both a close microphone and a room microphone,
and the instrument is loud enough in the room mic when playing loud, but you want to boost it when it is playing soft.
#### Test
```faust
co = library("compressors.lib");
os = library("oscillators.lib");
meter(x) = x;
FBcompressor_N_chan_test = (os.osc(440), os.osc(660)) : co.FBcompressor_N_chan(0.5, -12, 0.01, 0.1, 6, 0, 0.5, meter, 2);
```
#### References
* <http://en.wikipedia.org/wiki/Dynamic_range_compression>
* Digital Dynamic Range Compressor Design: A Tutorial and Analysis, Dimitrios GIANNOULIS (<Dimitrios.Giannoulis@eecs.qmul.ac.uk>), Michael MASSBERG (<michael@massberg.org>), and Josuah D.REISS (<josh.reiss@eecs.qmul.ac.uk>)

---

## co.FBFFcompressor_N_chan

--------------------`(co.)FBFFcompressor_N_chan`-------------------
Feed forward / feed back N channels dynamic range compressor.
The feedback part has a much higher strength, so they end up sounding similar.
`FBFFcompressor_N_chan` is a standard Faust function.
#### Usage
```faust
si.bus(N) : FBFFcompressor_N_chan(strength,thresh,att,rel,knee,prePost,link,FBFF,meter,N) : si.bus(N)
```
Where:
* `strength`: strength of the compression (0 = no compression, 1 means hard limiting, >1 means over-compression)
* `thresh`: dB level threshold above which compression kicks in
* `att`: attack time = time constant (sec) when level & compression going up
* `rel`: release time = time constant (sec) coming out of compression
* `knee`: a gradual increase in gain reduction around the threshold:
below thresh-(knee/2) there is no gain reduction,
above thresh+(knee/2) there is the same gain reduction as without a knee,
and in between there is a gradual increase in gain reduction
* `prePost`: places the level detector either at the input or after the gain computer;
this turns it from a linear return-to-zero detector into a log  domain return-to-threshold detector
* `link`: the amount of linkage between the channels: 0 = each channel is independent, 1 = all channels have the same amount of gain reduction
* `FBFF`: fade between feed forward (0) and feed back (1) compression
* `meter`: a gain reduction meter. It can be implemented like so:
`meter = _<:(_,(max(maxGR):meter_group((hbargraph("[1][unit:dB][tooltip: gain reduction in dB]", maxGR, 0))))):attach;`
* `N`: the number of channels of the compressor, known at compile time
It uses a strength parameter instead of the traditional ratio, in order to be able to
function as a hard limiter.
For that you'd need a ratio of infinity:1, and you cannot express that in Faust.
Sometimes even bigger ratios are useful:
for example a group recording where one instrument is recorded with both a close microphone and a room microphone,
and the instrument is loud enough in the room mic when playing loud, but you want to boost it when it is playing soft.
#### Test
```faust
co = library("compressors.lib");
os = library("oscillators.lib");
meter(x) = x;
FBFFcompressor_N_chan_test = (os.osc(440), os.osc(660)) : co.FBFFcompressor_N_chan(0.4, -12, 0.01, 0.1, 6, 0, 0.5, 0.3, meter, 2);
```
#### References
* <http://en.wikipedia.org/wiki/Dynamic_range_compression>
* Digital Dynamic Range Compressor Design: A Tutorial and Analysis, Dimitrios GIANNOULIS (<Dimitrios.Giannoulis@eecs.qmul.ac.uk>), Michael MASSBERG (<michael@massberg.org>), and Josuah D.REISS (<josh.reiss@eecs.qmul.ac.uk>)

---

## co.RMS_compression_gain_mono_db

--------------------`(co.)RMS_compression_gain_mono_db`-------------------
Mono RMS dynamic range compressor gain computer with dB output.
`RMS_compression_gain_mono_db` is a standard Faust function.
#### Usage
```faust
_ : RMS_compression_gain_mono_db(strength,thresh,att,rel,knee,prePost) : _
```
Where:
* `strength`: strength of the compression (0 = no compression, 1 means hard limiting, >1 means over-compression)
* `thresh`: dB level threshold above which compression kicks in
* `att`: attack time = time constant (sec) when level & compression going up
* `rel`: release time = time constant (sec) coming out of compression
* `knee`: a gradual increase in gain reduction around the threshold:
below thresh-(knee/2) there is no gain reduction,
above thresh+(knee/2) there is the same gain reduction as without a knee,
and in between there is a gradual increase in gain reduction
* `prePost`: places the level detector either at the input or after the gain computer;
this turns it from a linear return-to-zero detector into a log  domain return-to-threshold detector
It uses a strength parameter instead of the traditional ratio, in order to be able to
function as a hard limiter.
For that you'd need a ratio of infinity:1, and you cannot express that in Faust.
Sometimes even bigger ratios are useful:
for example a group recording where one instrument is recorded with both a close microphone and a room microphone,
and the instrument is loud enough in the room mic when playing loud, but you want to boost it when it is playing soft.
#### Test
```faust
co = library("compressors.lib");
os = library("oscillators.lib");
RMS_compression_gain_mono_db_test = os.osc(330) : co.RMS_compression_gain_mono_db(0.5, -18, 0.02, 0.12, 6, 0);
```
#### References
* <http://en.wikipedia.org/wiki/Dynamic_range_compression>
* Digital Dynamic Range Compressor Design: A Tutorial and Analysis, Dimitrios GIANNOULIS (<Dimitrios.Giannoulis@eecs.qmul.ac.uk>), Michael MASSBERG (<michael@massberg.org>), and Josuah D.REISS (<josh.reiss@eecs.qmul.ac.uk>)

---

## co.RMS_compression_gain_N_chan_db

--------------------`(co.)RMS_compression_gain_N_chan_db`-------------------
RMS N channels dynamic range compressor gain computer with dB output.
`RMS_compression_gain_N_chan_db` is a standard Faust function.
#### Usage
```faust
si.bus(N) : RMS_compression_gain_N_chan_db(strength,thresh,att,rel,knee,prePost,link,N) : si.bus(N)
```
Where:
* `strength`: strength of the compression (0 = no compression, 1 means hard limiting, >1 means over-compression)
* `thresh`: dB level threshold above which compression kicks in
* `att`: attack time = time constant (sec) when level & compression going up
* `rel`: release time = time constant (sec) coming out of compression
* `knee`: a gradual increase in gain reduction around the threshold:
below thresh-(knee/2) there is no gain reduction,
above thresh+(knee/2) there is the same gain reduction as without a knee,
and in between there is a gradual increase in gain reduction
* `prePost`: places the level detector either at the input or after the gain computer;
this turns it from a linear return-to-zero detector into a log  domain return-to-threshold detector
* `link`: the amount of linkage between the channels: 0 = each channel is independent, 1 = all channels have the same amount of gain reduction
* `N`: the number of channels of the compressor
It uses a strength parameter instead of the traditional ratio, in order to be able to
function as a hard limiter.
For that you'd need a ratio of infinity:1, and you cannot express that in Faust.
Sometimes even bigger ratios are useful:
for example a group recording where one instrument is recorded with both a close microphone and a room microphone,
and the instrument is loud enough in the room mic when playing loud, but you want to boost it when it is playing soft.
#### Test
```faust
co = library("compressors.lib");
os = library("oscillators.lib");
RMS_compression_gain_N_chan_db_test = (os.osc(330), os.osc(550)) : co.RMS_compression_gain_N_chan_db(0.5, -18, 0.02, 0.12, 6, 0, 0.5, 2);
```
#### References
* <http://en.wikipedia.org/wiki/Dynamic_range_compression>
* Digital Dynamic Range Compressor Design: A Tutorial and Analysis, Dimitrios GIANNOULIS (<Dimitrios.Giannoulis@eecs.qmul.ac.uk>), Michael MASSBERG (<michael@massberg.org>), and Josuah D.REISS (<josh.reiss@eecs.qmul.ac.uk>)

---

## co.RMS_FBFFcompressor_N_chan

--------------------`(co.)RMS_FBFFcompressor_N_chan`-------------------
RMS feed forward / feed back N channels dynamic range compressor.
The feedback part has a much higher strength, so they end up sounding similar.
`RMS_FBFFcompressor_N_chan` is a standard Faust function.
#### Usage
```faust
si.bus(N) : RMS_FBFFcompressor_N_chan(strength,thresh,att,rel,knee,prePost,link,FBFF,meter,N) : si.bus(N)
```
Where:
* `strength`: strength of the compression (0 = no compression, 1 means hard limiting, >1 means over-compression)
* `thresh`: dB level threshold above which compression kicks in
* `att`: attack time = time constant (sec) when level & compression going up
* `rel`: release time = time constant (sec) coming out of compression
* `knee`: a gradual increase in gain reduction around the threshold:
below thresh-(knee/2) there is no gain reduction,
above thresh+(knee/2) there is the same gain reduction as without a knee,
and in between there is a gradual increase in gain reduction
* `prePost`: places the level detector either at the input or after the gain computer;
this turns it from a linear return-to-zero detector into a log  domain return-to-threshold detector
* `link`: the amount of linkage between the channels: 0 = each channel is independent, 1 = all channels have the same amount of gain reduction
* `FBFF`: fade between feed forward (0) and feed back (1) compression.
* `meter`: a gain reduction meter. It can be implemented with:
`meter = _<:(_,(max(maxGR):meter_group((hbargraph("[1][unit:dB][tooltip: gain reduction in dB]", maxGR, 0))))):attach;`
* `N`: the number of channels of the compressor, known at compile time
It uses a strength parameter instead of the traditional ratio, in order to be able to
function as a hard limiter.
For that you'd need a ratio of infinity:1, and you cannot express that in Faust.
Sometimes even bigger ratios are useful:
for example a group recording where one instrument is recorded with both a close microphone and a room microphone,
and the instrument is loud enough in the room mic when playing loud, but you want to boost it when it is playing soft.
To save CPU we cheat a bit, in a similar way as in the original libs:
instead of crosfading between two sets of gain calculators as above,
we take the `abs` of the audio from both the FF and FB, and crossfade between those,
and feed that into one set of gain calculators
again the strength is much higher when in FB mode, but implemented differently.
#### Test
```faust
co = library("compressors.lib");
os = library("oscillators.lib");
meter(x) = x;
RMS_FBFFcompressor_N_chan_test = (os.osc(330), os.osc(550)) : co.RMS_FBFFcompressor_N_chan(0.4, -18, 0.02, 0.12, 6, 0, 0.5, 0.3, meter, 2);
```
#### References
* <http://en.wikipedia.org/wiki/Dynamic_range_compression>
* Digital Dynamic Range Compressor Design: A Tutorial and Analysis, Dimitrios GIANNOULIS (<Dimitrios.Giannoulis@eecs.qmul.ac.uk>), Michael MASSBERG (<michael@massberg.org>), and Josuah D.REISS (<josh.reiss@eecs.qmul.ac.uk>)

---

## co.RMS_FBcompressor_peak_limiter_N_chan

--------------------`(co.)RMS_FBcompressor_peak_limiter_N_chan`-------------------
N channel RMS feed back compressor into peak limiter feeding back into the FB compressor.
By combining them this way, they complement each other optimally:
the RMS compressor doesn't have to deal with the peaks,
and the peak limiter get's spared from the steady state signal.
The feedback part has a much higher strength, so they end up sounding similar.
`RMS_FBcompressor_peak_limiter_N_chan` is a standard Faust function.
#### Usage
```faust
si.bus(N) : RMS_FBcompressor_peak_limiter_N_chan(strength,thresh,threshLim,att,rel,knee,link,meter,meterLim,N) : si.bus(N)
```
Where:
* `strength`: strength of the compression (0 = no compression, 1 means hard limiting, >1 means over-compression)
* `thresh`: dB level threshold above which compression kicks in
* `threshLim`: dB level threshold above which the brickwall limiter kicks in
* `att`: attack time = time constant (sec) when level & compression going up
this is also used as the release time of the limiter
* `rel`: release time = time constant (sec) coming out of compression
* `knee`: a gradual increase in gain reduction around the threshold:
below thresh-(knee/2) there is no gain reduction,
above thresh+(knee/2) there is the same gain reduction as without a knee,
and in between there is a gradual increase in gain reduction
the limiter uses a knee half this size
* `link`: the amount of linkage between the channels: 0 = each channel is independent, 1 = all channels have the same amount of gain reduction
* `meter`: compressor gain reduction meter. It can be implemented with:
`meter = _<:(_,(max(maxGR):meter_group((hbargraph("[1][unit:dB][tooltip: gain reduction in dB]", maxGR, 0))))):attach;`
* `meterLim`: brickwall limiter gain reduction meter. It can be implemented with:
`meterLim = _<:(_,(max(maxGR):meter_group((hbargraph("[1][unit:dB][tooltip: gain reduction in dB]", maxGR, 0))))):attach;`
* `N`: the number of channels of the compressor, known at compile time
It uses a strength parameter instead of the traditional ratio, in order to be able to
function as a hard limiter.
For that you'd need a ratio of infinity:1, and you cannot express that in Faust.
Sometimes even bigger ratios are useful:
for example a group recording where one instrument is recorded with both a close microphone and a room microphone,
and the instrument is loud enough in the room mic when playing loud, but you want to boost it when it is playing soft.
#### Test
```faust
co = library("compressors.lib");
os = library("oscillators.lib");
meter(x) = x;
meterLim(x) = x;
RMS_FBcompressor_peak_limiter_N_chan_test = (os.osc(330), os.osc(550)) : co.RMS_FBcompressor_peak_limiter_N_chan(0.4, -18, -2, 0.02, 0.12, 6, 0.5, meter, meterLim, 2);
```
#### References
* <http://en.wikipedia.org/wiki/Dynamic_range_compression>
* Digital Dynamic Range Compressor Design: A Tutorial and Analysis, Dimitrios GIANNOULIS (<Dimitrios.Giannoulis@eecs.qmul.ac.uk>), Michael MASSBERG (<michael@massberg.org>), and Josuah D.REISS (<josh.reiss@eecs.qmul.ac.uk>)

---

## co.peak_compression_gain_mono

--------------------`(co.)peak_compression_gain_mono`-------------------
Mono dynamic range compressor gain computer with linear output.
`peak_compression_gain_mono` is a standard Faust function.
#### Usage
```faust
_ : peak_compression_gain_mono(strength,thresh,att,rel,knee,prePost) : _
```
Where:
* `strength`: strength of the compression (0 = no compression, 1 means hard limiting, >1 means over-compression)
* `thresh`: dB level threshold above which compression kicks in
* `att`: attack time = time constant (sec) when level & compression going up
* `rel`: release time = time constant (sec) coming out of compression
* `knee`: a gradual increase in gain reduction around the threshold:
below thresh-(knee/2) there is no gain reduction,
above thresh+(knee/2) there is the same gain reduction as without a knee,
and in between there is a gradual increase in gain reduction
* `prePost`: places the level detector either at the input or after the gain computer;
this turns it from a linear return-to-zero detector into a log  domain return-to-threshold detector
It uses a strength parameter instead of the traditional ratio, in order to be able to
function as a hard limiter.
For that you'd need a ratio of infinity:1, and you cannot express that in Faust.
Sometimes even bigger ratios are useful:
for example a group recording where one instrument is recorded with both a close microphone and a room microphone,
and the instrument is loud enough in the room mic when playing loud, but you want to boost it when it is playing soft.
#### Test
```faust
co = library("compressors.lib");
os = library("oscillators.lib");
peak_compression_gain_mono_test = os.osc(440) : co.peak_compression_gain_mono(0.5, -12, 0.01, 0.1, 6, 0);
```
#### References
* <http://en.wikipedia.org/wiki/Dynamic_range_compression>
* Digital Dynamic Range Compressor Design: A Tutorial and Analysis, Dimitrios GIANNOULIS (<Dimitrios.Giannoulis@eecs.qmul.ac.uk>), Michael MASSBERG (<michael@massberg.org>), and Josuah D.REISS (<josh.reiss@eecs.qmul.ac.uk>)

---

## co.peak_compression_gain_N_chan

--------------------`(co.)peak_compression_gain_N_chan`-------------------
N channels dynamic range compressor gain computer with linear output.
`peak_compression_gain_N_chan` is a standard Faust function.
#### Usage
```faust
si.bus(N) : peak_compression_gain_N_chan(strength,thresh,att,rel,knee,prePost,link,N) : si.bus(N)
```
Where:
* `strength`: strength of the compression (0 = no compression, 1 means hard limiting, >1 means over-compression)
* `thresh`: dB level threshold above which compression kicks in
* `att`: attack time = time constant (sec) when level & compression going up
* `rel`: release time = time constant (sec) coming out of compression
* `knee`: a gradual increase in gain reduction around the threshold:
below thresh-(knee/2) there is no gain reduction,
above thresh+(knee/2) there is the same gain reduction as without a knee,
and in between there is a gradual increase in gain reduction
* `prePost`: places the level detector either at the input or after the gain computer;
this turns it from a linear return-to-zero detector into a log  domain return-to-threshold detector
* `link`: the amount of linkage between the channels: 0 = each channel is independent, 1 = all channels have the same amount of gain reduction
* `N`: the number of channels of the compressor, known at compile time
It uses a strength parameter instead of the traditional ratio, in order to be able to
function as a hard limiter.
For that you'd need a ratio of infinity:1, and you cannot express that in Faust.
Sometimes even bigger ratios are useful:
for example a group recording where one instrument is recorded with both a close microphone and a room microphone,
and the instrument is loud enough in the room mic when playing loud, but you want to boost it when it is playing soft.
#### Test
```faust
co = library("compressors.lib");
os = library("oscillators.lib");
peak_compression_gain_N_chan_test = (os.osc(440), os.osc(660)) : co.peak_compression_gain_N_chan(0.5, -12, 0.01, 0.1, 6, 0, 0.5, 2);
```
#### References
* <http://en.wikipedia.org/wiki/Dynamic_range_compression>
* Digital Dynamic Range Compressor Design: A Tutorial and Analysis, Dimitrios GIANNOULIS (<Dimitrios.Giannoulis@eecs.qmul.ac.uk>), Michael MASSBERG (<michael@massberg.org>), and Josuah D.REISS (<josh.reiss@eecs.qmul.ac.uk>)
generalise compression gains for N channels.
first we define a mono version:

---

## co.RMS_compression_gain_mono

--------------------`(co.)RMS_compression_gain_mono`-------------------
Mono RMS dynamic range compressor gain computer with linear output.
`RMS_compression_gain_mono` is a standard Faust function.
#### Usage
```faust
_ : RMS_compression_gain_mono(strength,thresh,att,rel,knee,prePost) : _
```
Where:
* `strength`: strength of the compression (0 = no compression, 1 means hard limiting, >1 means over-compression)
* `thresh`: dB level threshold above which compression kicks in
* `att`: attack time = time constant (sec) when level & compression going up
* `rel`: release time = time constant (sec) coming out of compression
* `knee`: a gradual increase in gain reduction around the threshold:
below thresh-(knee/2) there is no gain reduction,
above thresh+(knee/2) there is the same gain reduction as without a knee,
and in between there is a gradual increase in gain reduction
* `prePost`: places the level detector either at the input or after the gain computer;
this turns it from a linear return-to-zero detector into a log  domain return-to-threshold detector
It uses a strength parameter instead of the traditional ratio, in order to be able to
function as a hard limiter.
For that you'd need a ratio of infinity:1, and you cannot express that in Faust.
Sometimes even bigger ratios are useful:
for example a group recording where one instrument is recorded with both a close microphone and a room microphone,
and the instrument is loud enough in the room mic when playing loud, but you want to boost it when it is playing soft.
#### Test
```faust
co = library("compressors.lib");
os = library("oscillators.lib");
RMS_compression_gain_mono_test = os.osc(330) : co.RMS_compression_gain_mono(0.5, -18, 0.02, 0.12, 6, 0);
```
#### References
* <http://en.wikipedia.org/wiki/Dynamic_range_compression>
* Digital Dynamic Range Compressor Design: A Tutorial and Analysis, Dimitrios GIANNOULIS (<Dimitrios.Giannoulis@eecs.qmul.ac.uk>), Michael MASSBERG (<michael@massberg.org>), and Josuah D.REISS (<josh.reiss@eecs.qmul.ac.uk>)

---

## co.RMS_compression_gain_N_chan

--------------------`(co.)RMS_compression_gain_N_chan`-------------------
RMS N channels dynamic range compressor gain computer with linear output.
`RMS_compression_gain_N_chan` is a standard Faust function.
#### Usage
```faust
si.bus(N) : RMS_compression_gain_N_chan(strength,thresh,att,rel,knee,prePost,link,N) : si.bus(N)
```
Where:
* `strength`: strength of the compression (0 = no compression, 1 means hard limiting, >1 means over-compression)
* `thresh`: dB level threshold above which compression kicks in
* `att`: attack time = time constant (sec) when level & compression going up
* `rel`: release time = time constant (sec) coming out of compression
* `knee`: a gradual increase in gain reduction around the threshold:
below thresh-(knee/2) there is no gain reduction,
above thresh+(knee/2) there is the same gain reduction as without a knee,
and in between there is a gradual increase in gain reduction
* `prePost`: places the level detector either at the input or after the gain computer;
this turns it from a linear return-to-zero detector into a log  domain return-to-threshold detector
* `link`: the amount of linkage between the channels: 0 = each channel is independent, 1 = all channels have the same amount of gain reduction
* `N`: the number of channels of the compressor, known at compile time
It uses a strength parameter instead of the traditional ratio, in order to be able to
function as a hard limiter.
For that you'd need a ratio of infinity:1, and you cannot express that in Faust.
Sometimes even bigger ratios are useful:
for example a group recording where one instrument is recorded with both a close microphone and a room microphone,
and the instrument is loud enough in the room mic when playing loud, but you want to boost it when it is playing soft.
#### Test
```faust
co = library("compressors.lib");
os = library("oscillators.lib");
RMS_compression_gain_N_chan_test = (os.osc(330), os.osc(550)) : co.RMS_compression_gain_N_chan(0.5, -18, 0.02, 0.12, 6, 0, 0.5, 2);
```
#### References
* <http://en.wikipedia.org/wiki/Dynamic_range_compression>
* Digital Dynamic Range Compressor Design: A Tutorial and Analysis, Dimitrios GIANNOULIS (<Dimitrios.Giannoulis@eecs.qmul.ac.uk>), Michael MASSBERG (<michael@massberg.org>), and Josuah D.REISS (<josh.reiss@eecs.qmul.ac.uk>)

---

## co.compressor_lad_mono

--------------------`(co.)compressor_lad_mono`-------------------
Mono dynamic range compressor with lookahead delay.
`compressor_lad_mono` is a standard Faust function.
#### Usage
```faust
_ : compressor_lad_mono(lad,ratio,thresh,att,rel) : _
```
Where:
* `lad`: lookahead delay in seconds (nonnegative) - gets rounded to nearest sample.
The effective attack time is a good setting
* `ratio`: compression ratio (1 = no compression, >1 means compression)
Ratios: 4 is moderate compression, 8 is strong compression,
12 is mild limiting, and 20 is pretty hard limiting at the threshold
* `thresh`: dB level threshold above which compression kicks in (0 dB = max level)
* `att`: attack time = time constant (sec) when level & compression are going up
* `rel`: release time = time constant (sec) coming out of compression
#### Test
```faust
co = library("compressors.lib");
os = library("oscillators.lib");
compressor_lad_mono_test = os.osc(440) : co.compressor_lad_mono(0.005, 4, -9, 0.01, 0.1);
```
#### References
* <http://en.wikipedia.org/wiki/Dynamic_range_compression>
* <https://ccrma.stanford.edu/~jos/filters/Nonlinear_Filter_Example_Dynamic.html>
* Albert Graef's "faust2pd"/examples/synth/compressor_.dsp
* More features: <https://github.com/magnetophon/faustCompressors>

---

## co.compressor_mono

--------------------`(co.)compressor_mono`-------------------
Mono dynamic range compressors.
`compressor_mono` is a standard Faust function.
#### Usage
```faust
_ : compressor_mono(ratio,thresh,att,rel) : _
```
Where:
* `ratio`: compression ratio (1 = no compression, >1 means compression)
Ratios: 4 is moderate compression, 8 is strong compression,
12 is mild limiting, and 20 is pretty hard limiting at the threshold
* `thresh`: dB level threshold above which compression kicks in (0 dB = max level)
* `att`: attack time = time constant (sec) when level & compression are going up
* `rel`: release time = time constant (sec) coming out of compression
#### Test
```faust
co = library("compressors.lib");
os = library("oscillators.lib");
compressor_mono_test = os.osc(440) : co.compressor_mono(4, -9, 0.01, 0.2);
```
#### References
* <http://en.wikipedia.org/wiki/Dynamic_range_compression>
* <https://ccrma.stanford.edu/~jos/filters/Nonlinear_Filter_Example_Dynamic.html>
* Albert Graef's "faust2pd"/examples/synth/compressor_.dsp
* More features: <https://github.com/magnetophon/faustCompressors>

---

## co.compressor_stereo

--------------------`(co.)compressor_stereo`-------------------
Stereo dynamic range compressors.
#### Usage
```faust
_,_ : compressor_stereo(ratio,thresh,att,rel) : _,_
```
Where:
* `ratio`: compression ratio (1 = no compression, >1 means compression)
* `thresh`: dB level threshold above which compression kicks in (0 dB = max level)
* `att`: attack time = time constant (sec) when level & compression going up
* `rel`: release time = time constant (sec) coming out of compression
#### Test
```faust
co = library("compressors.lib");
os = library("oscillators.lib");
compressor_stereo_test = (os.osc(440), os.osc(660)) : co.compressor_stereo(4, -9, 0.01, 0.2);
```
#### References
* <http://en.wikipedia.org/wiki/Dynamic_range_compression>
* <https://ccrma.stanford.edu/~jos/filters/Nonlinear_Filter_Example_Dynamic.html>
* Albert Graef's "faust2pd"/examples/synth/compressor_.dsp
* More features: <https://github.com/magnetophon/faustCompressors>

---

## co.compression_gain_mono

--------------------`(co.)compression_gain_mono`-------------------
Compression-gain calculation for dynamic range compressors.
#### Usage
```faust
_ : compression_gain_mono(ratio,thresh,att,rel) : _
```
Where:
* `ratio`: compression ratio (1 = no compression, >1 means compression)
* `thresh`: dB level threshold above which compression kicks in (0 dB = max level)
* `att`: attack time = time constant (sec) when level & compression going up
* `rel`: release time = time constant (sec) coming out of compression
#### Test
```faust
co = library("compressors.lib");
os = library("oscillators.lib");
compression_gain_mono_test = os.osc(440) : co.compression_gain_mono(4, -9, 0.01, 0.2);
```
#### References
* <http://en.wikipedia.org/wiki/Dynamic_range_compression>
* <https://ccrma.stanford.edu/~jos/filters/Nonlinear_Filter_Example_Dynamic.html>
* Albert Graef's "faust2pd"/examples/synth/compressor_.dsp
* More features: <https://github.com/magnetophon/faustCompressors>

---

## co.limiter_1176_R4_mono

----------------`(co.)limiter_1176_R4_mono`----------------------
A limiter guards against hard-clipping.  It can be
implemented as a compressor having a high threshold (near the
clipping level), fast attack, and high ratio.  Since
the compression ratio is so high, some knee smoothing is
desirable (for softer limiting).  This example is intended
to get you started using compressors as limiters, so all
parameters are hardwired here to nominal values.
`ratio`: 4 (moderate compression).
See `compressor_mono` comments for a guide to other choices.
Mike Shipley likes this (lowest) setting on the 1176.
(Grammy award-winning mixer for Queen, Tom Petty, etc.).
`thresh`: -6 dB, meaning 4:1 compression begins at amplitude 1/2.
`att`: 800 MICROseconds (Note: scaled by ratio in the 1176)
The 1176 range is said to be 20-800 microseconds.
Faster attack gives "more bite" (e.g. on vocals),
and makes hard-clipping less likely on fast overloads.
`rel`: 0.5 s (Note: scaled by ratio in the 1176)
The 1176 range is said to be 50-1100 ms.
The 1176 also has a "bright, clear eq effect" (use filters.lib if desired).
`limiter_1176_R4_mono` is a standard Faust function.
#### Usage
```faust
_ : limiter_1176_R4_mono : _
```
#### Test
```faust
co = library("compressors.lib");
os = library("oscillators.lib");
limiter_1176_R4_mono_test = os.osc(440) : co.limiter_1176_R4_mono;
```
#### References
* <http://en.wikipedia.org/wiki/1176_Peak_Limiter>

---

## co.limiter_1176_R4_stereo

-------------------`(co.)limiter_1176_R4_stereo`---------------------
A limiter guards against hard-clipping.  It can be
implemented as a compressor having a high threshold (near the
clipping level), fast attack and release, and high ratio.  Since
the ratio is so high, some knee smoothing is
desirable ("soft limiting").  This example is intended
to get you started using `compressor_*` as a limiter, so all
parameters are hardwired to nominal values here.
`ratio`: 4 (moderate compression), 8 (severe compression),
12 (mild limiting), or 20 to 1 (hard limiting).
`att`: 20-800 MICROseconds (Note: scaled by ratio in the 1176).
`rel`: 50-1100 ms (Note: scaled by ratio in the 1176).
Mike Shipley likes 4:1 (Grammy-winning mixer for Queen, Tom Petty, etc.)
Faster attack gives "more bite" (e.g. on vocals).
He hears a bright, clear eq effect as well (not implemented here).
#### Usage
```faust
_,_ : limiter_1176_R4_stereo : _,_
```
#### Test
```faust
co = library("compressors.lib");
os = library("oscillators.lib");
limiter_1176_R4_stereo_test = (os.osc(440), os.osc(660)) : co.limiter_1176_R4_stereo;
```
#### References
* <http://en.wikipedia.org/wiki/1176_Peak_Limiter>

---

## co.peak_expansion_gain_N_chan_db

--------------------`(co.)peak_expansion_gain_N_chan_db`-------------------
N channels dynamic range expander gain computer.
`peak_expansion_gain_N_chan_db` is a standard Faust function.
#### Usage
```faust
si.bus(N) : peak_expansion_gain_N_chan_db(strength,thresh,range,att,hold,rel,knee,prePost,link,maxHold,N) : si.bus(N)
```
Where:
* `strength`: strength of the expansion (0 = no expansion, 100 means gating, <1 means upward compression)
* `thresh`: dB level threshold below which expansion kicks in
* `range`: maximum amount of expansion in dB
* `att`: attack time = time constant (sec) coming out of expansion
* `hold` : hold time (sec)
* `rel`: release time = time constant (sec) going into expansion
* `knee`: a gradual increase in gain reduction around the threshold:
above thresh+(knee/2) there is no gain reduction,
below thresh-(knee/2) there is the same gain reduction as without a knee,
and in between there is a gradual increase in gain reduction
* `prePost`: places the level detector either at the input or after the gain computer;
this turns it from a linear return-to-zero detector into a log  domain return-to-range detector
* `link`: the amount of linkage between the channels: 0 = each channel is independent, 1 = all channels have the same amount of gain reduction
* `maxHold`: the maximum hold time in samples, known at compile time
* `N`: the number of channels of the gain computer, known at compile time
#### Test
```faust
co = library("compressors.lib");
os = library("oscillators.lib");
peak_expansion_gain_N_chan_db_test = (os.osc(220), os.osc(330)) : co.peak_expansion_gain_N_chan_db(0.5, -40, 20, 0.05, 0.01, 0.2, 6, 0, 0.5, 2048, 2);
```
generalise expansion gains for N channels.
first we define a mono version:

---

## co.expander_N_chan

--------------------`(co.)expander_N_chan`-------------------
Feed forward N channels dynamic range expander.
`expander_N_chan` is a standard Faust function.
#### Usage
```faust
si.bus(N) : expander_N_chan(strength,thresh,range,att,hold,rel,knee,prePost,link,meter,maxHold,N) : si.bus(N)
```
Where:
* `strength`: strength of the expansion (0 = no expansion, 100 means gating, <1 means upward compression)
* `thresh`: dB level threshold below which expansion kicks in
* `range`: maximum amount of expansion in dB
* `att`: attack time = time constant (sec) coming out of expansion
* `hold` : hold time
* `rel`: release time = time constant (sec) going into expansion
* `knee`: a gradual increase in gain reduction around the threshold:
above thresh+(knee/2) there is no gain reduction,
below thresh-(knee/2) there is the same gain reduction as without a knee,
and in between there is a gradual increase in gain reduction
* `prePost`: places the level detector either at the input or after the gain computer;
this turns it from a linear return-to-zero detector into a log  domain return-to-range detector
* `link`: the amount of linkage between the channels: 0 = each channel is independent, 1 = all channels have the same amount of gain reduction
* `meter`: a gain reduction meter. It can be implemented like so:
`meter = _<:(_, (ba.linear2db:max(maxGR):meter_group((hbargraph("[1][unit:dB][tooltip: gain reduction in dB]", maxGR, 0))))):attach;`
* `maxHold`: the maximum hold time in samples, known at compile time
* `N`: the number of channels of the expander, known at compile time
#### Test
```faust
co = library("compressors.lib");
os = library("oscillators.lib");
meter(x) = x;
expander_N_chan_test = (os.osc(220), os.osc(330)) : co.expander_N_chan(0.5, -40, 20, 0.05, 0.02, 0.2, 6, 0, 0.5, meter, 4096, 2);
```
Feed forward expander

---

## co.expanderSC_N_chan

--------------------`(co.)expanderSC_N_chan`-------------------
Feed forward N channels dynamic range expander with sidechain.
`expanderSC_N_chan` is a standard Faust function.
#### Usage
```faust
si.bus(N) : expanderSC_N_chan(strength,thresh,range,att,hold,rel,knee,prePost,link,meter,maxHold,N,SCfunction,SCswitch,SCsignal) : si.bus(N)
```
Where:
* `strength`: strength of the expansion (0 = no expansion, 100 means gating, <1 means upward compression)
* `thresh`: dB level threshold below which expansion kicks in
* `range`: maximum amount of expansion in dB
* `att`: attack time = time constant (sec) coming out of expansion
* `hold` : hold time
* `rel`: release time = time constant (sec) going into expansion
* `knee`: a gradual increase in gain reduction around the threshold:
above thresh+(knee/2) there is no gain reduction,
below thresh-(knee/2) there is the same gain reduction as without a knee,
and in between there is a gradual increase in gain reduction
* `prePost`: places the level detector either at the input or after the gain computer;
this turns it from a linear return-to-zero detector into a log  domain return-to-range detector
* `link`: the amount of linkage between the channels: 0 = each channel is independent, 1 = all channels have the same amount of gain reduction
* `meter`: a gain reduction meter. It can be implemented like so:
`meter = _<:(_, (ba.linear2db:max(maxGR):meter_group((hbargraph("[1][unit:dB][tooltip: gain reduction in dB]", maxGR, 0))))):attach;`
* `maxHold`: the maximum hold time in samples, known at compile time
* `N`: the number of channels of the expander, known at compile time
* `SCfunction` : a function that get's placed before the level-detector, needs to have a single input and output
* `SCswitch` : use either the regular audio input or the SCsignal as the input for the level detector
* `SCsignal` : an audio signal, to be used as the input for the level detector when SCswitch is 1
#### Test
```faust
co = library("compressors.lib");
os = library("oscillators.lib");
meter(x) = x;
SCfunction(x) = x;
expanderSC_N_chan_test = (os.osc(220), os.osc(330)) : co.expanderSC_N_chan(0.5, -40, 20, 0.05, 0.02, 0.2, 6, 0, 0.5, meter, 4096, 2, SCfunction, 1, os.osc(880));
```
Feed forward expander with sidechain

---

## co.limiter_lad_N

-----------------------`(co.)limiter_lad_N`---------------------------------
N-channels lookahead limiter inspired by IOhannes Zmölnig's post, which is
in turn based on the thesis by Peter Falkner "Entwicklung eines digitalen
Stereo-Limiters mit Hilfe des Signalprozessors DSP56001".
This version of the limiter uses a peak-holder with smoothed
attack and release based on tau time constant filters.
It is also possible to use a time constant that is `2PI*tau` by dividing
the attack and release times by `2PI`. This time constant allows for
the amplitude profile to reach `1 - e^(-2PI)` of the final
peak after the attack time. The input path can be delayed by the same
amount as the attack time to synchronise input and amplitude profile,
realising a system that is particularly effective as a colourless
(ideally) brickwall limiter.
Note that the effectiveness of the ceiling settings are dependent on
the other parameters, especially the time constant used for the
smoothing filters and the lookahead delay.
Similarly, the colourless characteristics are also dependent on attack,
hold, and release times. Since fluctuations above ~15 Hz are
perceived as timbral effects, [Vassilakis and Kendall 2010] it is
reasonable to set the attack time to 1/15 seconds for a smooth amplitude
modulation. On the other hand, the hold time can be set to the
peak-to-peak period of the expected lowest frequency in the signal,
which allows for minimal distortion of the low frequencies. The
release time can then provide a perceptually linear and gradual gain
increase determined by the user for any specific application.
The scaling factor for all the channels is determined by the loudest peak
between them all, so that amplitude ratios between the signals are kept.
#### Usage
```faust
si.bus(N) : limiter_lad_N(N, LD, ceiling, attack, hold, release) : si.bus(N)
```
Where:
* `N`: is the number of channels, known at compile-time
* `LD`: is the lookahead delay in seconds, known at compile-time
* `ceiling`: is the linear amplitude output limit
* `attack`: is the attack time in seconds
* `hold`: is the hold time in seconds
* `release`: is the release time in seconds
Example for a stereo limiter: `limiter_lad_N(2, .01, 1, .01, .1, 1);`
#### Test
```faust
co = library("compressors.lib");
os = library("oscillators.lib");
limiter_lad_N_test = (os.osc(440), os.osc(660)) : co.limiter_lad_N(2, 0.01, 1, 0.01, 0.05, 0.2);
```
#### References
* <http://iem.at/~zmoelnig/publications/limiter>

---

## co.limiter_lad_mono

-------------`(co.)limiter_lad_mono`----------------------------------------
Specialised case of `limiter_lad_N` mono limiter.
#### Usage
```faust
_ : limiter_lad_mono(LD, ceiling, attack, hold, release) : _
```
Where:
* `LD`: is the lookahead delay in seconds, known at compile-time
* `ceiling`: is the linear amplitude output limit
* `attack`: is the attack time in seconds
* `hold`: is the hold time in seconds
* `release`: is the release time in seconds
#### Test
```faust
co = library("compressors.lib");
os = library("oscillators.lib");
limiter_lad_mono_test = os.osc(440) : co.limiter_lad_mono(0.01, 1, 0.01, 0.05, 0.2);
```
#### References
* <http://iem.at/~zmoelnig/publications/limiter>

---

## co.limiter_lad_stereo

-------------`(co.)limiter_lad_stereo`--------------------------------------
Specialised case of `limiter_lad_N` stereo limiter.
#### Usage
```faust
_,_ : limiter_lad_stereo(LD, ceiling, attack, hold, release) : _,_
```
Where:
* `LD`: is the lookahead delay in seconds, known at compile-time
* `ceiling`: is the linear amplitude output limit
* `attack`: is the attack time in seconds
* `hold`: is the hold time in seconds
* `release`: is the release time in seconds
#### Test
```faust
co = library("compressors.lib");
os = library("oscillators.lib");
limiter_lad_stereo_test = (os.osc(440), os.osc(660)) : co.limiter_lad_stereo(0.01, 1, 0.01, 0.05, 0.2);

```
#### References
* <http://iem.at/~zmoelnig/publications/limiter>

---

## co.limiter_lad_quad

-------------`(co.)limiter_lad_quad`----------------------------------------
Specialised case of `limiter_lad_N` quadraphonic limiter.
#### Usage
```faust
si.bus(4) : limiter_lad_quad(LD, ceiling, attack, hold, release) : si.bus(4)
```
Where:
* `LD`: is the lookahead delay in seconds, known at compile-time
* `ceiling`: is the linear amplitude output limit
* `attack`: is the attack time in seconds
* `hold`: is the hold time in seconds
* `release`: is the release time in seconds
#### Test
```faust
co = library("compressors.lib");
os = library("oscillators.lib");
limiter_lad_quad_test = (os.osc(220), os.osc(330), os.osc(440), os.osc(550)) : co.limiter_lad_quad(0.01, 1, 0.01, 0.05, 0.2);
```
#### References
* <http://iem.at/~zmoelnig/publications/limiter>

---

## co.limiter_lad_bw

-------------`(co.)limiter_lad_bw`-----------------------------------------
Specialised case of `limiter_lad_N` and ready-to-use unit-amplitude mono
limiting function. This implementation, in particular, uses `2PI*tau`
time constant filters for attack and release smoothing with
synchronised input and gain signals.
This function's best application is to be used as a brickwall limiter with
the least colouring artefacts while keeping a not-so-slow release curve.
Tests have shown that, given a pop song with 60 dB of amplification
and a 0-dB-ceiling, the loudest peak recorded was ~0.38 dB.
#### Usage
```faust
_ : limiter_lad_bw : _
```
#### Test
```faust
co = library("compressors.lib");
os = library("oscillators.lib");
limiter_lad_bw_test = os.osc(440) : co.limiter_lad_bw;
```
#### References
* <http://iem.at/~zmoelnig/publications/limiter>

---

# delays.lib
**Prefix:** `de`

################################ delays.lib ##########################################
Delays library. Its official prefix is `de`.

This library provides reusable building blocks for delay-based processing:
single and multi-tap delays, fractional delays and utilities for echo and spatial effects.

The Delays library is organized into 4 sections:

* [Basic Delay Functions](#basic-delay-functions)
* [Lagrange Interpolation](#lagrange-interpolation)
* [Thiran Allpass Interpolation](#thiran-allpass-interpolation)
* [Others](#others)

#### References

* <https://github.com/grame-cncm/faustlibraries/blob/master/delays.lib>
########################################################################################

## de.delay

-------`(de.)delay`----------
Simple `d` samples delay where `n` is the maximum delay length as a number of
samples. Unlike the `@` delay operator, here the delay signal `d` is explicitly
bounded to the interval [0..n]. The consequence is that delay will compile even
if the interval of d can't be computed by the compiler.
`delay` is a standard Faust function.
#### Usage
```faust
_ : delay(n,d) : _
```
Where:
* `n`: the max delay length in samples
* `d`: the delay length in samples (integer)
#### Test
```faust
de = library("delays.lib");
os = library("oscillators.lib");
delay_test = os.osc(440) : de.delay(44100, 22050);
```
TODO: add MBH np2

---

## de.fdelay

-------`(de.)fdelay`----------
Simple `d` samples fractional delay based on 2 interpolated delay lines where `n` is
the maximum delay length as a number of samples.
`fdelay` is a standard Faust function.
#### Usage
```faust
_ : fdelay(n,d) : _
```
Where:
* `n`: the max delay length in samples
* `d`: the delay length in samples (float)
#### Test
```faust
de = library("delays.lib");
os = library("oscillators.lib");
fdelay_test = os.osc(440) : de.fdelay(44100, 22050.5);
```

---

## de.sdelay

--------------------------`(de.)sdelay`----------------------------
s(mooth)delay: a mono delay that doesn't click and doesn't
transpose when the delay time is changed.
#### Usage
```faust
_ : sdelay(n,it,d) : _
```
Where:
* `n`: the max delay length in samples
* `it`: interpolation time (in samples), for example 1024
* `d`: the delay length in samples (float)
#### Test
```faust
de = library("delays.lib");
os = library("oscillators.lib");
sdelay_test = os.osc(440) : de.sdelay(44100, 1024, 22050.5);
```

---

## de.prime_power_delays

------------------`(de.)prime_power_delays`----------------
Prime Power Delay Line Lengths.
#### Usage
```faust
si.bus(N) : prime_power_delays(N,pathmin,pathmax) : si.bus(N);
```
Where:
* `N`: positive integer up to 16 (for higher powers of 2, extend 'primes' array below)
* `pathmin`: minimum acoustic ray length in the reverberator (in meters)
* `pathmax`: maximum acoustic ray length (meters) - think "room size"
#### Test
```faust
de = library("delays.lib");
prime_power_delays_test = de.prime_power_delays(4, 1, 10);
```
#### References
* <https://ccrma.stanford.edu/~jos/pasp/Prime_Power_Delay_Line.html>

---

## de.multiTapSincDelay

----------------`(de.)multiTapSincDelay`-------------
Variable delay line using multi-tap sinc interpolation.
This function implements a continuously variable delay line by superposing (2K+2) auxiliary delayed signals
whose positions and gains are determined by a sinc-based interpolation method. It extends the traditional
crossfade delay technique to significantly reduce spectral coloration artifacts, which are problematic in
applications like Wave Field Synthesis (WFS) and auralization.
Operation:
- If tau1 and tau2 are very close (|tau2 - tau1| ≈ 0), a simple fixed fractional delay is applied
- Otherwise, a variable delay is synthesized by:
- Computing (2K+2) taps symmetrically distributed around tau1 and tau2
- Applying sinc-based weighting to each tap, based on its offset from the target interpolated delay tau
- Summing all the weighted taps to produce the output
Features:
- Smooth delay variation without introducing Doppler pitch shifts
- Significant reduction of comb-filter coloration compared to classical crossfading
- Switching between fixed and variable delay modes to ensure stability
#### Usage
```faust
_ : multiTapSincDelay(K, MaxDelay, tau1, tau2, alpha) : _
```
Where:
* `K (integer)`: number of auxiliary tap pairs (a constant numerical expression). Total number of taps = 2*K + 2
* `MaxDelay`: maximum allowable delay in samples (buffer size)
* `tau1`: initial delay in samples (can be fractional)
* `tau2`: target delay in samples (can be fractional)
* `alpha`: interpolation factor between tau1 and tau2 (in [0,1] with 0 = tau1, 1 = tau2)
#### Test
```faust
de = library("delays.lib");
os = library("oscillators.lib");
multiTapSincDelay_test = os.osc(440) : de.multiTapSincDelay(2, 4096, 1024.0, 1536.0, 0.5);
```
#### References
T. Carpentier, "Implementation of a continuously variable delay line by crossfading between several tap delays", 2024: <https://hal.science/hal-04646939>

---

# demos.lib
**Prefix:** `dm`

################################ demos.lib ##########################################
Demos library. Its official prefix is `dm`.

This library provides a collection of example DSP algorithms and demonstrations
used to illustrate Faust features, syntax, and best practices. It includes simple
oscillators, filters, effects, and synthesis examples useful for learning and testing.

The Demos library is organized into 6 sections:

* [Analyzers](#analyzers)
* [Filters](#filters)
* [Effects](#effects)
* [Reverbs](#reverbs)
* [Generators](#generators)
* [Motion](#motion)

#### References

* <https://github.com/grame-cncm/faustlibraries/blob/master/demos.lib>
########################################################################################

## dm.mth_octave_spectral_level_demo

----------------------`(dm.)mth_octave_spectral_level_demo`----------------------
Demonstrate mth_octave_spectral_level in a standalone GUI.
#### Usage
```faust
_ : mth_octave_spectral_level_demo(BandsPerOctave) : _
_ : spectral_level_demo : _ // 2/3 octave

```
#### Test
```faust
dm = library("demos.lib");
no = library("noises.lib");
mth_octave_spectral_level_demo_test = no.noise : dm.mth_octave_spectral_level_demo(1.5);
spectral_level_demo_test = no.noise : dm.spectral_level_demo;
```

---

## dm.parametric_eq_demo

--------------------------`(dm.)parametric_eq_demo`------------------------------
A parametric equalizer application.
#### Usage:
```faust
_ : parametric_eq_demo : _

```
#### Test
```faust
dm = library("demos.lib");
no = library("noises.lib");
parametric_eq_demo_test = no.noise : dm.parametric_eq_demo;
```

---

## dm.spectral_tilt_demo

-------------------`(dm.)spectral_tilt_demo`-----------------------
A spectral tilt application.
#### Usage
```faust
_ : spectral_tilt_demo(N) : _ 
```
Where:
* `N`: filter order (integer)
#### Test
```faust
dm = library("demos.lib");
no = library("noises.lib");
spectral_tilt_demo_test = no.noise : dm.spectral_tilt_demo(4);
```
All other parameters interactive

---

## dm.cubicnl_demo

---------------------------`(dm.)cubicnl_demo`--------------------------
Distortion demo application.
#### Usage:
```faust
_ : cubicnl_demo : _

```
#### Test
```faust
dm = library("demos.lib");
no = library("noises.lib");
cubicnl_demo_test = no.noise : dm.cubicnl_demo;
```

---

## dm.gate_demo

----------------------------`(dm.)gate_demo`-------------------------
Gate demo application.
#### Usage
```faust
_,_ : gate_demo : _,_

```
#### Test
```faust
dm = library("demos.lib");
no = library("noises.lib");
gate_demo_test = no.noise, no.noise : dm.gate_demo;
```

---

## dm.compressor_demo

----------------------------`(dm.)compressor_demo`-------------------------
Compressor demo application.
#### Usage
```faust
_,_ : compressor_demo : _,_

```
#### Test
```faust
dm = library("demos.lib");
no = library("noises.lib");
compressor_demo_test = no.noise, no.noise : dm.compressor_demo;
```

---

## dm.moog_vcf_demo

-------------------------`(dm.)moog_vcf_demo`---------------------------
Illustrate and compare all three Moog VCF implementations above.
#### Usage
```faust
_ : moog_vcf_demo : _
```
#### Test
```faust
dm = library("demos.lib");
os = library("oscillators.lib");
moog_vcf_demo_test = os.osc(440) : dm.moog_vcf_demo;
```

---

## dm.wah4_demo

-------------------------`(dm.)wah4_demo`---------------------------
Wah pedal application.
#### Usage
```faust
_ : wah4_demo : _
```
#### Test
```faust
dm = library("demos.lib");
os = library("oscillators.lib");
wah4_demo_test = os.osc(440) : dm.wah4_demo;
```

---

## dm.crybaby_demo

-------------------------`(dm.)crybaby_demo`---------------------------
Crybaby effect application.
#### Usage
```faust
_ : crybaby_demo : _
```
#### Test
```faust
dm = library("demos.lib");
os = library("oscillators.lib");
crybaby_demo_test = os.osc(440) : dm.crybaby_demo;
```

---

## dm.flanger_demo

-------------------------`(dm.)flanger_demo`---------------------------
Flanger effect application.
#### Usage
```faust
_,_ : flanger_demo : _,_
```
#### Test
```faust
dm = library("demos.lib");
os = library("oscillators.lib");
flanger_demo_test = os.osc(440), os.osc(442) : dm.flanger_demo;
```

---

## dm.phaser2_demo

-------------------------`(dm.)phaser2_demo`---------------------------
Phaser effect demo application.
#### Usage
```faust
_,_ : phaser2_demo : _,_
```
#### Test
```faust
dm = library("demos.lib");
os = library("oscillators.lib");
phaser2_demo_test = os.osc(440), os.osc(442) : dm.phaser2_demo;
```

---

## dm.tapeStop_demo

-------------------------`(dm.)tapeStop_demo`---------------------------
Stereo tape-stop effect.
#### Usage
```faust
_,_ : tapeStop_demo : _,_
```
#### Test
```faust
dm = library("demos.lib");
os = library("oscillators.lib");
tapeStop_demo_test = os.osc(440), os.osc(442) : dm.tapeStop_demo;
```

---

## dm.freeverb_demo

----------------------------`(dm.)freeverb_demo`-------------------------
Freeverb demo application.
#### Usage
```faust
_,_ : freeverb_demo : _,_
```
#### Test
```faust
dm = library("demos.lib");
os = library("oscillators.lib");
freeverb_demo_test = os.osc(440), os.osc(442) : dm.freeverb_demo;
```

---

## dm.springreverb_demo

---------------------------`(dm.)springreverb_demo`----------------------------
Mono spring-inspired reverb demo using `re.springreverb`.
#### Usage
```faust
_ : springreverb_demo : _
```
#### Test
```faust
dm = library("demos.lib");
os = library("oscillators.lib");
springreverb_demo_test = os.osc(220) : dm.springreverb_demo;
```

---

## dm.stereo_reverb_tester

---------------------`(dm.)stereo_reverb_tester`--------------------
Handy test inputs for reverberator demos below.
#### Usage
```faust
_,_ : stereo_reverb_tester(gui_group) : _,_
```
For suppressing the `gui_group` input, pass it as `!`.
(See `(dm.)fdnrev0_demo` for an example of its use).
#### Test
```faust
dm = library("demos.lib");
no = library("noises.lib");
stereo_reverb_tester_test = no.noise, no.noise : dm.stereo_reverb_tester(!);
```

---

## dm.fdnrev0_demo

-------------------------`(dm.)fdnrev0_demo`---------------------------
A reverb application using `fdnrev0`.
#### Usage
```faust
_,_,_,_ : fdnrev0_demo(N,NB,BBSO) : _,_
```
Where:
* `N`: feedback Delay Network (FDN) order / number of delay lines used =
order of feedback matrix / 2, 4, 8, or 16 [extend primes array below for
32, 64, ...]
* `NB`: number of frequency bands / Number of (nearly) independent T60 controls
/ Integer 3 or greater
* `BBSO` : butterworth band-split order / order of lowpass/highpass bandsplit
used at each crossover freq / odd positive integer
#### Test
```faust
dm = library("demos.lib");
no = library("noises.lib");
fdnrev0_demo_test = no.noise, no.noise : dm.fdnrev0_demo(16, 5, 3);
```

---

## dm.zita_rev_fdn_demo

---------------------------`(dm.)zita_rev_fdn_demo`------------------------------
Reverb demo application based on `zita_rev_fdn`.
#### Usage
```faust
si.bus(8) : zita_rev_fdn_demo : si.bus(8)
```
#### Test
```faust
dm = library("demos.lib");
os = library("oscillators.lib");
zita_rev_fdn_demo_test = par(i, 8, os.osc(440 + i)) : dm.zita_rev_fdn_demo;
```

---

## dm.zita_light

---------------------------`(dm.)zita_light`------------------------------
Light version of `dm.zita_rev1` with only 2 UI elements.
#### Usage
```faust
_,_ : zita_light : _,_
```
#### Test
```faust
dm = library("demos.lib");
os = library("oscillators.lib");
zita_light_test = os.osc(440), os.osc(442) : dm.zita_light;
```

---

## dm.zita_rev1

----------------------------------`(dm.)zita_rev1`------------------------------
Example GUI for `zita_rev1_stereo` (mostly following the Linux `zita-rev1` GUI).
Only the dry/wet and output level parameters are "dezippered" here. If
parameters are to be varied in real time, use `smooth(0.999)` or the like
in the same way.
#### Usage
```faust
_,_ : zita_rev1 : _,_
```
#### Test
```faust
dm = library("demos.lib");
os = library("oscillators.lib");
zita_rev1_test = os.osc(440), os.osc(442) : dm.zita_rev1;
```
#### References
* <http://www.kokkinizita.net/linuxaudio/zita-rev1-doc/quickguide.html>

---

## dm.vital_rev_demo

----------------------------------`(dm.)vital_rev_demo`------------------------------
Example GUI for `vital_rev` with all parameters exposed.
#### Usage
```faust
_,_ : vital_rev_demo : _,_

```
#### Test
```faust
dm = library("demos.lib");
os = library("oscillators.lib");
vital_rev_demo_test = os.osc(440), os.osc(442) : dm.vital_rev_demo;
```

---

## dm.reverbTank_demo

--------------------------`(dm.)reverbTank_demo`---------------------------
This is a stereo reverb following the "ReverbTank" example in [1],
although some parameter ranges and scaling have been adjusted.
It is an unofficial version of the Spin Semiconductor® Reverb.
Other relevant instructional material can be found in [2-4].
#### Usage
```faust
_,_ : reverbTank_demo : _,_
```
#### Test
```faust
dm = library("demos.lib");
os = library("oscillators.lib");
reverbTank_demo_test = os.osc(440), os.osc(442) : dm.reverbTank_demo;
```
#### References
* [1] Pirkle, W. C. (2019). Designing audio effect plugins in C++ (2nd ed.). Chapter 17.14.
* [2] Spin Semiconductor. (n.d.). Reverberation. Retrieved 2024-04-16, from <http://www.spinsemi.com/knowledge_base/effects.html#Reverberation>
* [3] Zölzer, U. (2022). Digital audio signal processing (3rd ed.). Chapter 7, Figure 7.39.
* [4] Valhalla DSP. (2010, August 25). RIP Keith Barr. Retrieved 2024-04-16, from <https://valhalladsp.com/2010/08/25/rip-keith-barr/>

---

## dm.kb_rom_rev1_demo

--------------------------`(dm.)kb_rom_rev1_demo`--------------------------
Keith Barr reverb effect rom_rev1 demo application.
#### Usage
```faust
_,_ : kb_rom_rev1_demo : _,_
```
#### Test
```faust
dm = library("demos.lib");
os = library("oscillators.lib");
kb_rom_rev1_demo_test = os.osc(440), os.osc(442) : dm.kb_rom_rev1_demo;
```

---

## dm.dattorro_rev_demo

----------------------------------`(dm.)dattorro_rev_demo`------------------------------
Example GUI for `dattorro_rev` with all parameters exposed and additional
dry/wet and output gain control.
#### Usage
```faust
_,_ : dattorro_rev_demo : _,_
```
#### Test
```faust
dm = library("demos.lib");
os = library("oscillators.lib");
dattorro_rev_demo_test = os.osc(440), os.osc(442) : dm.dattorro_rev_demo;
```

---

## dm.jprev_demo

----------------------------------`(dm.)jprev_demo`------------------------------
Example GUI for `jprev` with all parameters exposed.
#### Usage
```faust
_,_ : jprev_demo : _,_
```
#### Test
```faust
dm = library("demos.lib");
os = library("oscillators.lib");
jprev_demo_test = os.osc(440), os.osc(442) : dm.jprev_demo;
```

---

## dm.greyhole_demo

----------------------------------`(dm.)greyhole_demo`------------------------------
Example GUI for `greyhole` with all parameters exposed.
#### Usage
```faust
_,_ : greyhole_demo : _,_

```
#### Test
```faust
dm = library("demos.lib");
os = library("oscillators.lib");
greyhole_demo_test = os.osc(440), os.osc(442) : dm.greyhole_demo;
```

---

## dm.sawtooth_demo

--------------------------`(dm.)sawtooth_demo`---------------------------
An application demonstrating the different sawtooth oscillators of Faust.
#### Usage
```faust
sawtooth_demo : _
```
#### Test
```faust
dm = library("demos.lib");
sawtooth_demo_test = dm.sawtooth_demo;
```

---

## dm.virtual_analog_oscillator_demo

----------------------`(dm.)virtual_analog_oscillator_demo`----------------------
Virtual analog oscillator demo application.
#### Usage
```faust
virtual_analog_oscillator_demo : _
```
#### Test
```faust
dm = library("demos.lib");
virtual_analog_oscillator_demo_test = dm.virtual_analog_oscillator_demo;
```

---

## dm.velvet_noise_demo

--------------------------`(dm.)velvet_noise_demo`---------------------------
Listen to velvet_noise!
#### Usage
```faust
velvet_noise_demo : _
```
#### Test
```faust
dm = library("demos.lib");
velvet_noise_demo_test = dm.velvet_noise_demo;
```

---

## dm.latch_demo

--------------------------`(dm.)latch_demo`---------------------------
Illustrate latch operation.
#### Usage
```faust
echo 'import("stdfaust.lib");' > latch_demo.dsp
echo 'process = dm.latch_demo;' >> latch_demo.dsp
faust2octave latch_demo.dsp
Octave:1> plot(faustout);
```
#### Test
```faust
dm = library("demos.lib");
latch_demo_test = dm.latch_demo;
```

---

## dm.envelopes_demo

--------------------------`(dm.)envelopes_demo`---------------------------
Illustrate various envelopes overlaid, including their gate * 1.1.
#### Usage
```faust
echo 'import("stdfaust.lib");' > envelopes_demo.dsp
echo 'process = dm.envelopes_demo;' >> envelopes_demo.dsp
faust2octave envelopes_demo.dsp
Octave:1> plot(faustout);
```
#### Test
```faust
dm = library("demos.lib");
envelopes_demo_test = dm.envelopes_demo;
```

---

## dm.fft_spectral_level_demo

-------------------`(dm.)fft_spectral_level_demo`------------------
Make a real-time spectrum analyzer using FFT from analyzers.lib.
#### Usage
```faust
echo 'import("stdfaust.lib");' > fft_spectral_level_demo.dsp
echo 'process = dm.fft_spectral_level_demo;' >> fft_spectral_level_demo.dsp
Mac:
faust2caqt fft_spectral_level_demo.dsp
open fft_spectral_level_demo.app
Linux GTK:
faust2jack fft_spectral_level_demo.dsp
./fft_spectral_level_demo
Linux QT:
faust2jaqt fft_spectral_level_demo.dsp
./fft_spectral_level_demo
```
#### Test
```faust
dm = library("demos.lib");
fft_spectral_level_demo_test = dm.fft_spectral_level_demo(256);
```

---

## dm.pospass_demo

------------------------`(dm.)pospass_demo`------------------------
Use Positive-Pass Filter pospass() to frequency-shift a sine tone.
First, a real sinusoid is converted to its analytic-signal form
using pospass() to filter out its negative frequency component.
Next, it is multiplied by a modulating complex sinusoid at the
shifting frequency to create the frequency-shifted result.
The real and imaginary parts are output to channels 1 & 2.
For a more interesting frequency-shifting example, check the
"Use Mic" checkbox to replace the input sinusoid by mic input.
Note that frequency shifting is not the same as frequency scaling.
A frequency-shifted harmonic signal is usually not harmonic.
Very small frequency shifts give interesting chirp effects when
there is feedback around the frequency shifter.
#### Usage
```faust
echo 'import("stdfaust.lib");' > pospass_demo.dsp
echo 'process = dm.pospass_demo;' >> pospass_demo.dsp
Mac:
faust2caqt pospass_demo.dsp
open pospass_demo.app
Linux GTK:
faust2jack pospass_demo.dsp
./pospass_demo
Linux QT:
faust2jaqt pospass_demo.dsp
./pospass_demo
Etc.
```
#### Test
```faust
dm = library("demos.lib");
os = library("oscillators.lib");
pospass_demo_test = os.osc(440) : dm.pospass_demo;
```

---

## dm.exciter

-------------------------------`(dm.)exciter`-------------------------------
Psychoacoustic harmonic exciter, with GUI.
#### Usage
```faust
_ : exciter : _

```
#### Test
```faust
dm = library("demos.lib");
no = library("noises.lib");
exciter_test = no.noise : dm.exciter;
```
#### References
* <https://secure.aes.org/forum/pubs/ebriefs/?elib=16939>
* <https://www.researchgate.net/publication/258333577_Modeling_the_Harmonic_Exciter>

---

## dm.vocoder_demo

----------------------------`(dm.)vocoder_demo`-------------------------
Use example of the vocoder function where an impulse train is used
as excitation.
#### Usage
```faust
_ : vocoder_demo : _

```
#### Test
```faust
dm = library("demos.lib");
os = library("oscillators.lib");
no = library("noises.lib");
vocoder_demo_test = no.noise : dm.vocoder_demo;
```

---

## dm.colored_noise_demo

-----------------`(dm.)colored_noise_demo`--------------------
A coloured noise signal generator.
#### Usage
```faust
colored_noise_demo : _
```
#### Test
```faust
dm = library("demos.lib");
colored_noise_demo_test = dm.colored_noise_demo;
```

---

## dm.shock_trigger_demo

-----------------`(dm.)shock_trigger_demo`--------------------
Debounced shock trigger driving a tone. UI:
- [Auto Pulse] synths periodic impacts.
- [Pulse Rate] sets the tempo.
- [Axis Offset] trims the accelerometer input before HP/threshold.
- [High-pass], [Threshold], [Debounce] shape the trigger window.
- [Tone Frequency] sets the audible indicator driven by the shock gate.
#### Usage
```faust
shock_trigger_demo : _
```
#### Test
```faust
dm = library("demos.lib");
shock_trigger_demo_test = dm.shock_trigger_demo;
```

---

## dm.projected_gravity_demo

-----------------`(dm.)projected_gravity_demo`--------------------
Gravity projection mapped to a low-pass filter sweep. UI:
- [Auto Tilt] + [Tilt Rate]/[Tilt Depth] synthesize rocking.
- [Axis Offset] biases the axis.
- [Low-pass] controls smoothing before projection
- [Offset] sets the dead-zone.
- [Noise Level] sets bed loudness; projection modulates filter cutoff.
#### Usage
```faust
projected_gravity_demo : _
```
#### Test
```faust
dm = library("demos.lib");
projected_gravity_demo_test = dm.projected_gravity_demo;
```

---

## dm.total_accel_demo

-----------------`(dm.)total_accel_demo`--------------------
Total acceleration envelope mapped to noise amplitude. UI:
- [Auto Motion] + per-axis rates/depth synthesize movement; per-axis offsets bias inputs.
- [Threshold]/[Gain] set envelope detection.
- [Attack]/[Release] smooth it.
- Envelope scales the saw tone amplitude.
#### Usage
```faust
total_accel_demo : _
```
#### Test
```faust
dm = library("demos.lib");
total_accel_demo_test = dm.total_accel_demo;
```

---

## dm.orientation6_demo

-----------------`(dm.)orientation6_demo`--------------------
Six-axis orientation weights mapped to six tonal channels. UI:
- [Auto Orbit] + [Orbit Rate]/[Depth] synthesize a 3D path; X/Y/Z knobs add offsets.
- Six [Shape ...] knobs tighten/loosen each face’s lobe.
- [Smooth] sets response time.
- Each weight drives a distinct tone channel.
#### Usage
```faust
orientation6_demo : _,_,_,_,_,_
```
#### Test
```faust
dm = library("demos.lib");
orientation6_demo_test = dm.orientation6_demo;
```

---

## dm.motion_wrapper_demo

-----------------`(dm.)motion_wrapper_demo`--------------------
End-to-end motion feature monitor built on motion.lib:
- Ingests six 3-axis IMUs (left arm, feet, back, right arm, head, stomach).
- Derives shock triggers, inclinometers, projected gravity, accel/gyro envelopes,
six-face orientation weights per sensor, and raw/scaled axis taps.
- Exposes 92 UI-gated outputs matching the motion.lib signal names.
#### Usage
```faust
motion_wrapper_demo :
(leftArm_x,  leftArm_y,  leftArm_z,
feet_x,     feet_y,     feet_z,
back_x,     back_y,     back_z,
rightArm_x, rightArm_y, rightArm_z,
head_x,     head_y,     head_z,
stomach_x,  stomach_y,  stomach_z) -> 92 outputs
```
#### Test
```faust
dm = library("demos.lib");
motion_wrapper_demo_test = dm.motion_wrapper_demo;
```

---

# doc.lib
**Prefix:** `do`

##################################### doc.lib ##########################################
This library is used to generate the documentation of the Faust standard libraries.
########################################################################################

# envelopes.lib
**Prefix:** `en`

################################ envelopes.lib ##########################################
Envelopes library. Its official prefix is `en`.

This library provides envelope generators and control functions for shaping
signal amplitude, pitch, or other parameters. It includes ADSR, AR, and percussive
models, as well as exponential, linear, and segmented envelope types used in both
synthesis and dynamic processing contexts.

The Envelopes library is organized into 3 sections:

* [Envelopes with linear segments](#envelopes-with-linear-segments)
* [Envelopes with exponential segments](#envelopes-with-exponential-segments)
* [Others](#others)

#### References

* <https://github.com/grame-cncm/faustlibraries/blob/master/envelopes.lib>
########################################################################################

## en.ar

-----------------------`(en.)ar`--------------------------
AR (Attack, Release) envelope generator (useful to create percussion envelopes).
`ar` is a standard Faust function.
#### Usage
```faust
ar(at,rt,t) : _
```
Where:
* `at`: attack (sec)
* `rt`: release (sec)
* `t`: trigger signal (attack is triggered when `t>0`, release is triggered
when the envelope value reaches 1)
#### Test
```faust
en = library("envelopes.lib");
no = library("noises.lib");
ar_test = no.noise * en.ar(0.02, 0.3, button("gate"));
```

---

## en.asr

------------------------`(en.)asr`----------------------
ASR (Attack, Sustain, Release) envelope generator.
`asr` is a standard Faust function.
#### Usage
```faust
asr(at,sl,rt,t) : _
```
Where:
* `at`: attack (sec)
* `sl`: sustain level (between 0..1)
* `rt`: release (sec)
* `t`: trigger signal (attack is triggered when `t>0`, release is triggered
when `t=0`)
#### Test
```faust
en = library("envelopes.lib");
no = library("noises.lib");
asr_test = no.noise * en.asr(0.05, 0.7, 0.4, button("gate"));
```

---

## en.adsr

------------------------`(en.)adsr`----------------------
ADSR (Attack, Decay, Sustain, Release) envelope generator.
`adsr` is a standard Faust function.
#### Usage
```faust
adsr(at,dt,sl,rt,t) : _
```
Where:
* `at`: attack time (sec)
* `dt`: decay time (sec)
* `sl`: sustain level (between 0..1)
* `rt`: release time (sec)
* `t`: trigger signal (attack is triggered when `t>0`, release is triggered
when `t=0`)
#### Test
```faust
en = library("envelopes.lib");
no = library("noises.lib");
adsr_test = no.noise * en.adsr(0.05, 0.1, 0.6, 0.3, button("gate"));
```

---

## en.adsrf_bias

------------------------`(en.)adsrf_bias`------------------------------
ADSR (Attack, Decay, Sustain, Release, Final) envelope generator with
control over bias on each segment, and toggle for legato.
#### Usage
```faust
adsrf_bias(at,dt,sl,rt,final,b_att,b_dec,b_rel,legato,t) : _
```
Where:
* `at`: attack time (sec)
* `dt`: decay time (sec)
* `sl`: sustain level (between 0..1)
* `rt`: release time (sec)
* `final`: final level (between 0..1) but less than or equal to `sl`
* `b_att`: bias during attack (between 0..1) where 0.5 is no bias.
* `b_dec`: bias during decay (between 0..1) where 0.5 is no bias.
* `b_rel`: bias during release (between 0..1) where 0.5 is no bias.
* `legato`: toggle for legato. If disabled, envelopes "re-trigger" from zero.
* `t`: trigger signal (attack is triggered when `t>0`, release is triggered
when `t=0`)
#### Test
```faust
en = library("envelopes.lib");
no = library("noises.lib");
adsrf_bias_test = no.noise * en.adsrf_bias(
0.05, 0.1, 0.6, 0.4, 0.2,
0.4, 0.6, 0.5,
checkbox("legato"), button("gate")
);
```

---

## en.adsr_bias

------------------------`(en.)adsr_bias`------------------------------
ADSR (Attack, Decay, Sustain, Release) envelope generator with
control over bias on each segment, and toggle for legato.
#### Usage
```faust
adsr_bias(at,dt,sl,rt,b_att,b_dec,b_rel,legato,t) : _
```
Where:
* `at`: attack time (sec)
* `dt`: decay time (sec)
* `sl`: sustain level (between 0..1)
* `rt`: release time (sec)
* `b_att`: bias during attack (between 0..1) where 0.5 is no bias.
* `b_dec`: bias during decay (between 0..1) where 0.5 is no bias.
* `b_rel`: bias during release (between 0..1) where 0.5 is no bias.
* `legato`: toggle for legato. If disabled, envelopes "re-trigger" from zero.
* `t`: trigger signal (attack is triggered when `t>0`, release is triggered
when `t=0`)
#### Test
```faust
en = library("envelopes.lib");
no = library("noises.lib");
adsr_bias_test = no.noise * en.adsr_bias(
0.05, 0.1, 0.6, 0.4,
0.4, 0.6, 0.5,
checkbox("legato"), button("gate")
);
```

---

## en.ahdsrf_bias

------------------------`(en.)ahdsrf_bias`---------------------------
AHDSR (Attack, Hold, Decay, Sustain, Release, Final) envelope generator
with control over bias on each segment, and toggle for legato.
#### Usage
```faust
ahdsrf_bias(at,ht,dt,sl,rt,final,b_att,b_dec,b_rel,legato,t) : _
```
Where:
* `at`: attack time (sec)
* `ht`: hold time (sec)
* `dt`: decay time (sec)
* `sl`: sustain level (between 0..1)
* `rt`: release time (sec)
* `final`: final level (between 0..1) but less than or equal to `sl`
* `b_att`: bias during attack (between 0..1) where 0.5 is no bias.
* `b_dec`: bias during decay (between 0..1) where 0.5 is no bias.
* `b_rel`: bias during release (between 0..1) where 0.5 is no bias.
* `legato`: toggle for legato. If disabled, envelopes "re-trigger" from zero.
* `t`: trigger signal (attack is triggered when `t>0`, release is triggered
when `t=0`)
#### Test
```faust
en = library("envelopes.lib");
no = library("noises.lib");
ahdsrf_bias_test = no.noise * en.ahdsrf_bias(
0.05, 0.05, 0.1, 0.6, 0.4, 0.2,
0.4, 0.6, 0.5,
checkbox("legato"), button("gate")
);
```

---

## en.ahdsr_bias

------------------------`(en.)ahdsr_bias`---------------------------
AHDSR (Attack, Hold, Decay, Sustain, Release) envelope generator
with control over bias on each segment, and toggle for legato.
#### Usage
```faust
ahdsr_bias(at,ht,dt,sl,rt,final,b_att,b_dec,b_rel,legato,t) : _
```
Where:
* `at`: attack time (sec)
* `ht`: hold time (sec)
* `dt`: decay time (sec)
* `sl`: sustain level (between 0..1)
* `rt`: release time (sec)
* `final`: final level (between 0..1) but less than or equal to `sl`
* `b_att`: bias during attack (between 0..1) where 0.5 is no bias.
* `b_dec`: bias during decay (between 0..1) where 0.5 is no bias.
* `b_rel`: bias during release (between 0..1) where 0.5 is no bias.
* `legato`: toggle for legato. If disabled, envelopes "re-trigger" from zero.
* `t`: trigger signal (attack is triggered when `t>0`, release is triggered
when `t=0`)
#### Test
```faust
en = library("envelopes.lib");
no = library("noises.lib");
ahdsr_bias_test = no.noise * en.ahdsr_bias(
0.05, 0.05, 0.1, 0.6, 0.4,
0.4, 0.6, 0.5,
checkbox("legato"), button("gate")
);
```

---

## en.smoothEnvelope

------------------------`(en.)smoothEnvelope`------------------------
An envelope with an exponential attack and release.
`smoothEnvelope` is a standard Faust function.
#### Usage
```faust
smoothEnvelope(ar,t) : _
```
Where:
* `ar`: attack and release duration (sec)
* `t`: trigger signal (attack is triggered when `t>0`, release is triggered
when `t=0`)
#### Test
```faust
en = library("envelopes.lib");
no = library("noises.lib");
smoothEnvelope_test = no.noise * en.smoothEnvelope(0.2, button("gate"));
```

---

## en.arfe

------------------------`(en.)arfe`----------------------
ARFE (Attack and Release-to-Final-value Exponentially) envelope generator.
Approximately equal to `smoothEnvelope(Attack/6.91)` when Attack == Release.
#### Usage
```faust
arfe(at,rt,fl,t) : _
```
Where:
* `at`: attack (sec)
* `rt`: release (sec)
* `fl`: final level to approach upon release (such as 0)
* `t`: trigger signal (attack is triggered when `t>0`, release is triggered
when `t=0`)
#### Test
```faust
en = library("envelopes.lib");
no = library("noises.lib");
arfe_test = no.noise * en.arfe(0.2, 0.4, 0, button("gate"));
```

---

## en.are

------------------------`(en.)are`----------------------
ARE (Attack, Release) envelope generator with Exponential segments.
Approximately equal to `smoothEnvelope(Attack/6.91)` when Attack == Release.
#### Usage
```faust
are(at,rt,t) : _
```
Where:
* `at`: attack (sec)
* `rt`: release (sec)
* `t`: trigger signal (attack is triggered when `t>0`, release is triggered
when `t=0`)
#### Test
```faust
en = library("envelopes.lib");
no = library("noises.lib");
are_test = no.noise * en.are(0.2, 0.4, button("gate"));
```

---

## en.asre

------------------------`(en.)asre`----------------------
ASRE (Attack, Sustain, Release) envelope generator with Exponential segments.
#### Usage
```faust
asre(at,sl,rt,t) : _
```
Where:
* `at`: attack (sec)
* `sl`: sustain level (between 0..1)
* `rt`: release (sec)
* `t`: trigger signal (attack is triggered when `t>0`, release is triggered
when `t=0`)
#### Test
```faust
en = library("envelopes.lib");
no = library("noises.lib");
asre_test = no.noise * en.asre(0.2, 0.6, 0.4, button("gate"));
```

---

## en.adsre

------------------------`(en.)adsre`----------------------
ADSRE (Attack, Decay, Sustain, Release) envelope generator with Exponential
segments.
#### Usage
```faust
adsre(at,dt,sl,rt,t) : _
```
Where:
* `at`: attack (sec)
* `dt`: decay (sec)
* `sl`: sustain level (between 0..1)
* `rt`: release (sec)
* `t`: trigger signal (attack is triggered when `t>0`, release is triggered
when `t=0`)
#### Test
```faust
en = library("envelopes.lib");
no = library("noises.lib");
adsre_test = no.noise * en.adsre(0.2, 0.1, 0.6, 0.4, button("gate"));
```

---

## en.ahdsre

------------------------`(en.)ahdsre`----------------------
AHDSRE (Attack, Hold, Decay, Sustain, Release) envelope generator with Exponential
segments.
#### Usage
```faust
ahdsre(at,ht,dt,sl,rt,t) : _
```
Where:
* `at`: attack (sec)
* `ht`: hold (sec)
* `dt`: decay (sec)
* `sl`: sustain level (between 0..1)
* `rt`: release (sec)
* `t`: trigger signal (attack is triggered when `t>0`, release is triggered
when `t=0`)
#### Test
```faust
en = library("envelopes.lib");
no = library("noises.lib");
ahdsre_test = no.noise * en.ahdsre(0.2, 0.05, 0.1, 0.6, 0.4, button("gate"));
```

---

## en.dx7envelope

----------------------`(en.)dx7envelope`----------------------
DX7 operator envelope generator with 4 independent rates and levels. It is
essentially a 4 points BPF.
#### Usage
```faust
dx7_envelope(R1,R2,R3,R4,L1,L2,L3,L4,t) : _
```
Where:
* `RN`: rates in seconds
* `LN`: levels (0-1)
* `t`: trigger signal
#### Test
```faust
en = library("envelopes.lib");
os = library("oscillators.lib");
dx7envelope_test = en.dx7envelope(
0.05, 0.1, 0.1, 0.2,
1, 0.8, 0.6, 0,
button("gate")
) * os.osc(440);
```

---

# fds.lib
**Prefix:** `fd`

############################# fds.lib ######################################
This library allows to build linear, explicit finite difference schemes
physical models in 1 or 2 dimensions using an approach based on the cellular
automata formalism. Its official prefix is `fd`.

In order to use the library, one needs to discretize the linear partial
differential equation of the desired system both at boundaries and in-between
them, thus obtaining a set of explicit recursion relations. Each one
of these will provide, for each spatial point the scalar coefficients to be
multiplied by the states of the current and past neighbour points.

Coefficients need to be stacked in parallel in order to form a coefficients
matrix for each point in the mesh. It is necessary to provide one matrix for
coefficients matrices are defined, they need to be placed in parallel and
ordered following the desired mesh structure (i.e., coefficients for the top
left boundaries will come first, while bottom right boundaries will come
last), to form a *coefficients scheme*, which can be used with the library
functions.

## Sources

Here are listed some works on finite difference schemes and cellular
automata thet were the basis for the implementation of this library

* S. Bilbao, Numerical Sound Synthesis.Chichester, UK: John Wiley Sons,
Ltd, 2009

* P. Narbel, "Qualitative and quantitative cellular automata from
differential equations," Lecture Notes in Computer Science, vol. 4173,
pp. 112–121, 10 2006

* X.-S. Yang and Y. Young, Cellular Automata, PDEs, and Pattern Formation.
Chapman & Hall/CRC, 092005, ch. 18, pp. 271–282.

The FDS library is organized into 5 sections:

* [Model Construction](#model-construction)
* [Interpolation](#interpolation)
* [Routing](#routing)
* [Scheme Operations](#scheme-operations)
* [Interaction Models](#interaction-models)

#### References

* <https://github.com/grame-cncm/faustlibraries/blob/master/fds.lib>
#############################################################################

## fd.model1D

--------------------------------`(fd.)model1D`-------------------------------
This function can be used to obtain a physical model in 1 dimension.
Takes a force input signal for each point and outputs the state of each
point.
#### Usage
```faust
si.bus(points) : model1D(points,R,T,scheme) : si.bus(points)
```
Where:
* `points`: size of the mesh in points
* `R`: neighbourhood radius, indicates how many side points are needed (i.e.
if R=1 the mesh depends on one point on the left and one on the right)
* `T`: time coefficient, indicates how much steps back in time are needed (i.
e. if T=1 the maximum delay needed for a neighbour state is 1 sample)
* `scheme`: coefficients scheme
#### Test
```faust
fd = library("fds.lib");
si = library("signals.lib");

scheme = 0, 0;
model1D_test = si.bus(2)
: fd.model1D(2, 0, 0, scheme)
: si.bus(2);
```

---

## fd.model2D

--------------------------------`(fd.)model2D`-------------------------------
This function can be used to obtain a physical model in 2 dimension.
Takes a force input signal for each point and outputs the state of each
point.
IMPORTANT: 2D models with more than 30x20 points might crash the c++
compiler. 2D models need to be compiled with the command line compiler,
the online one presents some issues.
#### Usage
```faust
si.bus(pointsX*pointsY) : model2D(pointsX,pointsY,R,T,scheme) :
si.bus(pointsX*pointsY)
```
Where:
* `pointsX`: horizontal size of the mesh in points
* `pointsY`: vertical size of the mesh in points
* `R`: neighbourhood radius, indicates how many side points are needed (i.e.
if R=1 the mesh depends on one point on the left and one on the right)
* `T`: time coefficient, indicates how much steps back in time are needed (i.
e. if T=1 the maximum delay needed for a neighbour state is 1 sample)
* `scheme`: coefficients scheme
#### Test
```faust
fd = library("fds.lib");
si = library("signals.lib");

scheme = 0, 0, 0, 0;
model2D_test = si.bus(4)
: fd.model2D(2, 2, 0, 0, scheme)
: si.bus(4);
```

---

## fd.stairsInterp1D

-----------------------------`(fd.)stairsInterp1D`---------------------------
Stairs interpolator in 1 dimension. Takes a number of signals and outputs
the same number of signals, where each one is multiplied by zero except the
one specified by the argument. This can vary at run time (i.e. a slider),
but must be an integer.
#### Usage
```faust
si.bus(points) : stairsInterp1D(points,point) : si.bus(points)
```
Where:
* `points`: total number of points in the mesh
* `point`: number of the desired nonzero signal
#### Test
```faust
fd = library("fds.lib");
si = library("signals.lib");

stairsInterp1D_test = si.bus(4)
: fd.stairsInterp1D(4, 1);
```

---

## fd.stairsInterp2D

-----------------------------`(fd.)stairsInterp2D`---------------------------
Stairs interpolator in 2 dimensions. Similar to the 1-D version.
#### Usage
```faust
si.bus(pointsX*pointsY) : stairsInterp2D(pointsX,pointsY,pointX,pointY) :
si.bus(pointsX*pointsY)
```
Where:
* `pointsX`: total number of points in the X direction
* `pointsY`: total number of points in the Y direction
* `pointX`: horizontal index of the desired nonzero signal
* `pointY`: vertical index of the desired nonzero signal
#### Test
```faust
fd = library("fds.lib");
si = library("signals.lib");

stairsInterp2D_test = si.bus(4)
: fd.stairsInterp2D(2, 2, 1, 0);
```

---

## fd.linInterp1D

-----------------------------`(fd.)linInterp1D`---------------------------
Linear interpolator in 1 dimension. Takes a number of signals and outputs
the same number of signals, where each one is multiplied by zero except two
signals around a floating point index. This is essentially a Faust
implementation of the $J(x_i)$ operator, not scaled by the spatial step.
(see Stefan Bilbao's book, Numerical Sound Synthesis). The index can vary
at run time.
#### Usage
```faust
si.bus(points) : linInterp1D(points,point) : si.bus(points)
```
Where:
* `points`: total number of points in the mesh
* `point`: floating point index
#### Test
```faust
fd = library("fds.lib");
si = library("signals.lib");

linInterp1D_test = si.bus(4)
: fd.linInterp1D(4, 1.25);
```

---

## fd.linInterp2D

-----------------------------`(fd.)linInterp2D`---------------------------
Linear interpolator in 2 dimensions. Similar to the 1 D version.
#### Usage
```faust
si.bus(pointsX*pointsY) : linInterp2D(pointsX,pointsY,pointX,pointY) :
si.bus(pointsX*pointsY)
```
Where:
* `pointsX`: total number of points in the X direction
* `pointsY`: total number of points in the Y direction
* `pointX`: horizontal float index
* `pointY`: vertical float index
#### Test
```faust
fd = library("fds.lib");
si = library("signals.lib");

linInterp2D_test = si.bus(4)
: fd.linInterp2D(2, 2, 0.6, 1.2);
```

---

## fd.stairsInterp1DOut

---------------------------`(fd.)stairsInterp1DOut`--------------------------
Stairs interpolator in 1 dimension. Similar to `stairsInterp1D`, except it
outputs only the desired signal.
#### Usage
```faust
si.bus(points) : stairsInterp1DOut(points,point) : _
```
Where:
* `points`: total number of points in the mesh
* `point`: number of the desired nonzero signal
#### Test
```faust
fd = library("fds.lib");
si = library("signals.lib");

stairsInterp1DOut_test = si.bus(4)
: fd.stairsInterp1DOut(4, 2);
```

---

## fd.stairsInterp2DOut

---------------------------`(fd.)stairsInterp2DOut`--------------------------
Stairs interpolator in 2 dimensions which outputs only one signal.
#### Usage
```faust
si.bus(pointsX*pointsY) : stairsInterp2DOut(pointsX,pointsY,pointX,pointY) : _
```
Where:
* `pointsX`: total number of points in the X direction
* `pointsY`: total number of points in the Y direction
* `pointX`: horizontal index of the desired nonzero signal
* `pointY`: vertical index of the desired nonzero signal
#### Test
```faust
fd = library("fds.lib");
si = library("signals.lib");

stairsInterp2DOut_test = si.bus(4)
: fd.stairsInterp2DOut(2, 2, 1, 0);
```

---

## fd.linInterp1DOut

---------------------------`(fd.)linInterp1DOut`--------------------------
Linear interpolator in 1 dimension. Similar to `stairsInterp1D`, except it
sums each output signal and provides only one output value.
#### Usage
```faust
si.bus(points) : linInterp1DOut(points,point) : _
```
Where:
* `points`: total number of points in the mesh
* `point`: floating point index
#### Test
```faust
fd = library("fds.lib");
si = library("signals.lib");

linInterp1DOut_test = si.bus(4)
: fd.linInterp1DOut(4, 1.5);
```

---

## fd.stairsInterp2DOut

---------------------------`(fd.)stairsInterp2DOut`--------------------------
Linear interpolator in 2 dimensions which outputs only one signal.
#### Usage
```faust
si.bus(pointsX*pointsY) : linInterp2DOut(pointsX,pointsY,pointX,pointY) : _
```
Where:
* `pointsX`: total number of points in the X direction
* `pointsY`: total number of points in the Y direction
* `pointX`: horizontal float index
* `pointY`: vertical float index
#### Test
```faust
fd = library("fds.lib");
si = library("signals.lib");

linInterp2DOut_test = si.bus(4)
: fd.linInterp2DOut(2, 2, 0.6, 1.2);
```

---

## fd.route1D

---------------------------------`(fd.)route1D`------------------------------
Routing function for 1 dimensional schemes.
#### Usage
```faust
si.bus((2*R+1)*(T+1)*points),si.bus(points*2) : route1D(points, R, T) :
si.bus((1 + ((2*R+1)*(T+1)) + (2*R+1))*points)
```
Where:
* `points`: total number of points in the mesh
* `R`: neighbourhood radius
* `T`: time coefficient
#### Test
```faust
fd = library("fds.lib");
si = library("signals.lib");

route1D_test = par(i, 3, 0)
: fd.route1D(1, 0, 0)
: si.bus(3);
```

---

## fd.route2D

--------------------------------`(fd.)route2D`-------------------------------
Routing function for 2 dimensional schemes.
#### Usage
```faust
si.bus((2*R+1)^2*(T+1)*pointsX*pointsY),si.bus(pointsX*pointsY*2) :
route2D(pointsX, pointsY, R, T) :
si.bus((1 + ((2*R+1)^2*(T+1)) + (2*R+1)^2)*pointsX*pointsY)
```
Where:
* `pointsX`: total number of points in the X direction
* `pointsY`: total number of points in the Y direction
* `R`: neighbourhood radius
* `T`: time coefficient
#### Test
```faust
fd = library("fds.lib");
si = library("signals.lib");

route2D_test = par(i, 3, 0)
: fd.route2D(1, 1, 0, 0)
: si.bus(3);
```

---

## fd.schemePoint

------------------------------`(fd.)schemePoint`-----------------------------
This function calculates the next state for each mesh point, in order to
form a scheme, several of these blocks need to be stacked in parallel.
This function takes in input, in order, the force, the coefficient matrices
and the neighbours’ signals and outputs the next point state.
#### Usage
```faust
_,si.bus((2*R+1)^D*(T+1)),si.bus((2*R+1)^D) : schemePoint(R,T,D) : _
```
Where:
* `R`: neighbourhood radius
* `T`: time coefficient
* `D`: scheme spatial dimensions (i.e. 1 if 1-D, 2 if 2-D)
#### Test
```faust
fd = library("fds.lib");
si = library("signals.lib");

schemePoint_test = par(i, 3, 0)
: fd.schemePoint(0, 0, 1);
```

---

## fd.buildScheme1D

------------------------------`(fd.)buildScheme1D`---------------------------
This function is used to stack in parallel several schemePoint functions in
1 dimension, according to the number of points.
#### Usage
```faust
si.bus((1 + ((2*R+1)*(T+1)) + (2*R+1))*points) : buildScheme1D(points,R,T) :
si.bus(points)
```
Where:
* `points`: total number of points in the mesh
* `R`: neighbourhood radius
* `T`: time coefficient
#### Test
```faust
fd = library("fds.lib");
si = library("signals.lib");

buildScheme1D_test = par(i, 3, 0)
: fd.buildScheme1D(1, 0, 0);
```

---

## fd.buildScheme2D

------------------------------`(fd.)buildScheme2D`---------------------------
This function is used to stack in parallel several schemePoint functions in
2 dimensions, according to the number of points in the X and Y directions.
#### Usage
```faust
si.bus((1 + ((2*R+1)^2*(T+1)) + (2*R+1)^2)*pointsX*pointsY) :
buildScheme2D(pointsX,pointsY,R,T) : si.bus(pointsX*pointsY)
```
Where:
* `pointsX`: total number of points in the X direction
* `pointsY`: total number of points in the Y direction
* `R`: neighbourhood radius
* `T`: time coefficient
#### Test
```faust
fd = library("fds.lib");
si = library("signals.lib");

buildScheme2D_test = par(i, 3, 0)
: fd.buildScheme2D(1, 1, 0, 0);
```

---

## fd.hammer

---------------------------------`(fd.)hammer`-------------------------------
Implementation of a nonlinear collision model. The hammer is essentially a
finite difference scheme of a linear damped oscillator, which is coupled
with the mesh through the collision model (see Stefan Bilbao's book,
Numerical Sound Synthesis).
#### Usage
```faust
_ :hammer(coeff,omega0Sqr,sigma0,kH,alpha,k,offset,fIn) : _
```
Where:
* `coeff`: output force scaling coefficient
* `omega0Sqr`: squared angular frequency of the hammer oscillator
* `sigma0`: damping coefficient of the hammer oscillator
* `kH`: hammer stiffness coefficient
* `alpha`: nonlinearity parameter
* `k`: time sampling step (the same as for the mesh)
* `offset`: distance between the string and the hammer at rest in meters
* `fIn`: hammer excitation signal (i.e. a button)
#### Test
```faust
fd = library("fds.lib");
os = library("oscillators.lib");

hammer_test = os.osc(5)
: fd.hammer(
0.1,
1000,
0.01,
1e5,
2.0,
1.0/48000,
0.001,
button("hammer:trigger")
);
```

---

## fd.bow

---------------------------------`(fd.)bow`-------------------------------
Implementation of a nonlinear friction based interaction model that induces
Helmholtz motion. (see Stefan Bilbao's book, Numerical Sound Synthesis).
#### Usage
```faust
_ :bow(coeff,alpha,k,vb) : _
```
Where:
* `coeff`: output force scaling coefficient
* `alpha`: nonlinearity parameter
* `k`: time sampling step (the same as for the mesh)
* `vb`: bow velocity [m/s]
#### Test
```faust
fd = library("fds.lib");
os = library("oscillators.lib");

bow_test = os.osc(5)
: fd.bow(0.05, 2.0, 1.0/48000, 0.1);
```

---

# filters.lib
**Prefix:** `fi`

##################################### filters.lib ########################################
Filters library. Its official prefix is `fi`.

This library provides a comprehensive collection of linear and nonlinear
filters used in audio and signal processing. It includes low-pass, high-pass,
band-pass, allpass, shelving, equalizer, and crossover filters, as well as advanced
analog and digital filter design sections for both educational and production use.

The Filters library is organized into 23 sections:

* [Basic Filters](#basic-filters)
* [Comb Filters](#comb-filters)
* [Direct-Form Digital Filter Sections](#direct-form-digital-filter-sections)
* [Direct-Form Second-Order Biquad Sections](#direct-form-second-order-biquad-sections)
* [Ladder/Lattice Digital Filters](#ladderlattice-digital-filters)
* [Useful Special Cases](#useful-special-cases)
* [Ladder/Lattice Allpass Filters](#ladderlattice-allpass-filters)
* [Digital Filter Sections Specified as Analog Filter Sections](#digital-filter-sections-specified-as-analog-filter-sections)
* [Simple Resonator Filters](#simple-resonator-filters)
* [Butterworth Lowpass/Highpass Filters](#butterworth-lowpasshighpass-filters)
* [Special Filter-Bank Delay-Equalizing Allpass Filters](#special-filter-bank-delay-equalizing-allpass-filters)
* [Elliptic (Cauer) Lowpass Filters](#elliptic-cauer-lowpass-filters)
* [Elliptic Highpass Filters](#elliptic-highpass-filters)
* [Butterworth Bandpass/Bandstop Filters](#butterworth-bandpassbandstop-filters)
* [Elliptic Bandpass Filters](#elliptic-bandpass-filters)
* [Parametric Equalizers (Shelf, Peaking)](#parametric-equalizers-shelf-peaking)
* [Mth-Octave Filter-Banks](#mth-octave-filter-banks)
* [Arbitrary-Crossover Filter-Banks and Spectrum Analyzers](#arbitrary-crossover-filter-banks-and-spectrum-analyzers)
* [State Variable Filters (SVF)](#state-variable-filters)
* [Linkwitz-Riley 4th-order 2-way, 3-way, and 4-way crossovers](#linkwitz-riley-4th-order-2-way-3-way-and-4-way-crossovers)
* [Standardized Filters](#standardized-filters)
* [Averaging Functions](#averaging-functions)
* [Kalman Filters](#kalman-filters)

#### References

* <https://github.com/grame-cncm/faustlibraries/blob/master/filters.lib>
########################################################################################
NOTE ABOUT LICENSES:
Each function in this library has its own license. Licenses are declared
before each function. Corresponding license terms can be found at the
bottom of this file or in the Faust libraries documentation.

## fi.zero

----------------------`(fi.)zero`--------------------------
One zero filter. Difference equation: \(y(n) = x(n) - zx(n-1)\).
#### Usage
```faust
_ : zero(z) : _
```
Where:
* `z`: location of zero along real axis in z-plane
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
zero_test = os.osc(440) : fi.zero(0.5);
```
#### References
<https://ccrma.stanford.edu/~jos/filters/One_Zero.html>

---

## fi.pole

------------------------`(fi.)pole`---------------------------
One pole filter. Could also be called a "leaky integrator".
Difference equation: \(y(n) = x(n) + py(n-1)\).
#### Usage
```faust
_ : pole(p) : _
```
Where:
* `p`: pole location = feedback coefficient
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
pole_test = os.osc(440) : fi.pole(0.9);
```
#### References
<https://ccrma.stanford.edu/~jos/filters/One_Pole.html>

---

## fi.integrator

----------------------`(fi.)integrator`--------------------------
Same as `pole(1)` [implemented separately for block-diagram clarity].
#### Usage
```faust
_ : integrator : _
```
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
integrator_test = os.osc(440) : fi.integrator;
```

---

## fi.dcblockerat

-------------------`(fi.)dcblockerat`-----------------------
DC blocker with configurable "break frequency".
The amplitude response is substantially flat above `fb`,
and sloped at about +6 dB/octave below `fb`.
Derived from the analog transfer function:
$$H(s) = \frac{s}{(s + 2 \pi f_b)}$$
(which can be seen as a 1st-order Butterworth highpass filter)
by the low-frequency-matching bilinear transform method
(i.e., using the typical frequency-scaling constant `2*SR`).
#### Usage
```faust
_ : dcblockerat(fb) : _
```
Where:
* `fb`: "break frequency" in Hz, i.e., -3 dB gain frequency (see 2nd reference below)
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
dcblockerat_test = os.osc(440) : fi.dcblockerat(30);
```
#### References
* <https://ccrma.stanford.edu/~jos/pasp/Bilinear_Transformation.html>
* <https://ccrma.stanford.edu/~jos/spectilt/Bode_Plots.html>

---

## fi.dcblocker

----------------------`(fi.)dcblocker`--------------------------
DC blocker. Default dc blocker has -3dB point near 35 Hz (at 44.1 kHz)
and high-frequency gain near 1.0025 (due to no scaling).
`dcblocker` is as standard Faust function.
#### Usage
```faust
_ : dcblocker : _
```
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
dcblocker_test = os.osc(440) : fi.dcblocker;
```

---

## fi.lptN

----------------------------`(fi.)lptN`--------------------------------------
One-pole lowpass filter with arbitrary dis/charging factors set in dB and
times set in seconds.
#### Usage
```faust
_ : lptN(N, tN) : _
```
Where:
* `N`: is the attenuation factor in dB
* `tN`: is the filter period in seconds, that is, the time for the
impulse response to decay by `N` dB
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
lptN_test = os.osc(440) : fi.lptN(60, 0.1);
```
#### References
<https://ccrma.stanford.edu/~jos/mdft/Exponentials.html>

---

## fi.lptau

------------------------`(fi.)lptau`--------------------------
One-pole lowpass with a tau time constant (1/e attenuation after `tN` seconds).
#### Usage
```faust
_ : lptau(tN) : _
```
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
lptau_test = os.osc(440) : fi.lptau(0.1);
```

---

## fi.lpt60

------------------------`(fi.)lpt60`--------------------------
One-pole lowpass with a T60 time constant (60 dB attenuation after `tN` seconds).
#### Usage
```faust
_ : lpt60(tN) : _
```
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
lpt60_test = os.osc(440) : fi.lpt60(0.3);
```

---

## fi.lpt19

------------------------`(fi.)lpt19`--------------------------
One-pole lowpass with a T19 time constant (approx. 19 dB attenuation after `tN` seconds).
#### Usage
```faust
_ : lpt19(tN) : _
```
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
lpt19_test = os.osc(440) : fi.lpt19(0.2);
```

---

## fi.ff_comb

------`(fi.)ff_comb`--------
Feed-Forward Comb Filter. Note that `ff_comb` requires integer delays
(uses `delay`  internally).
`ff_comb` is a standard Faust function.
#### Usage
```faust
_ : ff_comb(maxdel,intdel,b0,bM) : _
```
Where:
* `maxdel`: maximum delay (a power of 2)
* `intdel`: current (integer) comb-filter delay between 0 and maxdel
* `del`: current (float) comb-filter delay between 0 and maxdel
* `b0`: gain applied to delay-line input
* `bM`: gain applied to delay-line output and then summed with input
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
ff_comb_test = os.osc(440) : fi.ff_comb(2048, 64, 1, 0.7);
```
#### References
<https://ccrma.stanford.edu/~jos/pasp/Feedforward_Comb_Filters.html>

---

## fi.ff_fcomb

------`(fi.)ff_fcomb`--------
Feed-Forward Comb Filter. Note that `ff_fcomb` takes floating-point delays
(uses `fdelay` internally).
`ff_fcomb` is a standard Faust function.
#### Usage
```faust
_ : ff_fcomb(maxdel,del,b0,bM) : _
```
Where:
* `maxdel`: maximum delay (a power of 2)
* `del`: current (float) comb-filter delay between 0 and maxdel
* `b0`: gain applied to delay-line input
* `bM`: gain applied to delay-line output and then summed with input
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
ff_fcomb_test = os.osc(440) : fi.ff_fcomb(2048, 64.5, 1, 0.7);
```
#### References
<https://ccrma.stanford.edu/~jos/pasp/Feedforward_Comb_Filters.html>

---

## fi.ffcombfilter

-----------`(fi.)ffcombfilter`-------------------
Typical special case of `ff_comb()` where: `b0 = 1`.
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
ffcombfilter_test = os.osc(440) : fi.ffcombfilter(2048, 64, 0.7);
```

---

## fi.fb_comb_common

---------------------`(fi.)fb_comb_common`---------------------
A generic feedback comb filter.
#### Usage
```faust
_ : fb_comb_common(dop,N,b0,aN) : _
```
Where
* `dop`: delay operator, e.g. `@` or `de.fdelay4a(2048)`
* `N`: current delay
* `b0`: gain applied to input
* `aN`: gain applied to delay-line output
#### Example test program
```faust
process = fb_comb_common(@,N,b0,aN);
```
implements the following difference equation:
```faust
y[n] = b0 x[n] + aN y[n - N]
```
See more examples in `filters.lib` below.
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
fb_comb_common_test = os.osc(440) : fi.fb_comb_common(@, 64, 0.8, 0.6);
```

---

## fi.fb_comb

-----------------------`(fi.)fb_comb`-----------------------
Feed-Back Comb Filter (integer delay).
#### Usage
```faust
_ : fb_comb(maxdel,del,b0,aN) : _
```
Where:
* `maxdel`: maximum delay (a power of 2)
* `del`: current (float) comb-filter delay between 0 and maxdel
* `b0`: gain applied to delay-line input and forwarded to output
* `aN`: minus the gain applied to delay-line output before summing with the input
and feeding to the delay line
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
fb_comb_test = os.osc(440) : fi.fb_comb(2048, 64, 0.7, 0.6);
```
#### References
<https://ccrma.stanford.edu/~jos/pasp/Feedback_Comb_Filters.html>

---

## fi.fb_fcomb

-----------------------`(fi.)fb_fcomb`-----------------------
Feed-Back Comb Filter (floating point delay).
#### Usage
```faust
_ : fb_fcomb(maxdel,del,b0,aN) : _
```
Where:
* `maxdel`: maximum delay (a power of 2)
* `del`: current (float) comb-filter delay between 0 and maxdel
* `b0`: gain applied to delay-line input and forwarded to output
* `aN`: minus the gain applied to delay-line output before summing with the input
and feeding to the delay line
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
fb_fcomb_test = os.osc(440) : fi.fb_fcomb(2048, 64.5, 0.7, 0.6);
```
#### References
<https://ccrma.stanford.edu/~jos/pasp/Feedback_Comb_Filters.html>

---

## fi.rev1

-----------------------`(fi.)rev1`-----------------------
Special case of `fb_comb` (`rev1(maxdel,N,g)`).
The "rev1 section" dates back to the 1960s in computer-music reverberation.
See the `jcrev` and `brassrev` in `reverbs.lib` for usage examples.
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
rev1_test = os.osc(440) : fi.rev1(2048, 64, 0.6);
```

---

## fi.allpass_comb

-------------------`(fi.)allpass_comb`-----------------
Schroeder Allpass Comb Filter. Note that:
```faust
allpass_comb(maxlen,len,aN) = ff_comb(maxlen,len,aN,1) : fb_comb(maxlen,len-1,1,aN);
```
which is a direct-form-1 implementation, requiring two delay lines.
The implementation here is direct-form-2 requiring only one delay line.
#### Usage
```faust
_ : allpass_comb(maxdel,intdel,aN) : _
```
Where:
* `maxdel`: maximum delay (a power of 2)
* `intdel`: current (integer) comb-filter delay between 0 and maxdel
* `del`: current (float) comb-filter delay between 0 and maxdel
* `aN`: minus the feedback gain
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
allpass_comb_test = os.osc(440) : fi.allpass_comb(2048, 64, 0.6);
```
#### References
* <https://ccrma.stanford.edu/~jos/pasp/Allpass_Two_Combs.html>
* <https://ccrma.stanford.edu/~jos/pasp/Schroeder_Allpass_Sections.html>
* <https://ccrma.stanford.edu/~jos/filters/Four_Direct_Forms.html>

---

## fi.allpass_fcomb

-------------------`(fi.)allpass_fcomb`-----------------
Schroeder Allpass Comb Filter. Note that:
```faust
allpass_comb(maxlen,len,aN) = ff_comb(maxlen,len,aN,1) : fb_comb(maxlen,len-1,1,aN);
```
which is a direct-form-1 implementation, requiring two delay lines.
The implementation here is direct-form-2 requiring only one delay line.
`allpass_fcomb` is a standard Faust library.
#### Usage
```faust
_ : allpass_comb(maxdel,intdel,aN) : _
_ : allpass_fcomb(maxdel,del,aN) : _
```
Where:
* `maxdel`: maximum delay (a power of 2)
* `intdel`: current (float) comb-filter delay between 0 and maxdel
* `del`: current (float) comb-filter delay between 0 and maxdel
* `aN`: minus the feedback gain
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
allpass_fcomb_test = os.osc(440) : fi.allpass_fcomb(2048, 64.5, 0.6);
```
#### References
* <https://ccrma.stanford.edu/~jos/pasp/Allpass_Two_Combs.html>
* <https://ccrma.stanford.edu/~jos/pasp/Schroeder_Allpass_Sections.html>
* <https://ccrma.stanford.edu/~jos/filters/Four_Direct_Forms.html>

---

## fi.rev2

-----------------------`(fi.)rev2`-----------------------
Special case of `allpass_comb` (`rev2(maxlen,len,g)`).
The "rev2 section" dates back to the 1960s in computer-music reverberation.
See the `jcrev` and `brassrev` in `reverbs.lib` for usage examples.
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
rev2_test = os.osc(440) : fi.rev2(2048, 64, 0.6);
```

---

## fi.iir

----------------------------`(fi.)iir`-------------------------------
Nth-order Infinite-Impulse-Response (IIR) digital filter,
implemented in terms of the Transfer-Function (TF) coefficients.
Such filter structures are termed "direct form".
`iir` is a standard Faust function.
#### Usage
```faust
_ : iir(bcoeffs,acoeffs) : _
```
Where:
* `bcoeffs`: (b0,b1,...,b_order) = TF numerator coefficients
* `acoeffs`: (a1,...,a_order) = TF denominator coeffs (a0=1)
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
iir_test = os.osc(440) : fi.iir((0.5, 0.5), (0.3));
```
#### References
<https://ccrma.stanford.edu/~jos/filters/Four_Direct_Forms.html>

---

## fi.fir

-----------------------------`(fi.)fir`---------------------------------
FIR filter (convolution of FIR filter coefficients with a signal). `fir` is standard Faust function.
#### Usage
```faust
_ : fir(bv) : _
```
Where:
* `bv` = b0,b1,...,bn is a parallel bank of coefficient signals.
#### Note
`bv` is processed using pattern-matching at compile time,
so it must have this normal form (parallel signals).
#### Example test program
Smoothing white noise with a five-point moving average:
```faust
bv = .2,.2,.2,.2,.2;
process = noise : fir(bv);
```
Equivalent (note double parens):
```faust
process = noise : fir((.2,.2,.2,.2,.2));
```
fir(bv) = conv(bv);
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
fir_test = os.osc(440) : fi.fir((0.2, 0.2, 0.2, 0.2, 0.2));
```

---

## fi.notchw

------------`(fi.)notchw`--------------
Simple notch filter based on a biquad (`tf2`).
`notchw` is a standard Faust function.
#### Usage:
```faust
_ : notchw(width,freq) : _
```
Where:
* `width`: "notch width" in Hz (approximate)
* `freq`: "notch frequency" in Hz
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
notchw_test = os.osc(440) : fi.notchw(200, 1000);
```
#### References
<https://ccrma.stanford.edu/~jos/pasp/Phasing_2nd_Order_Allpass_Filters.html>

---

## fi.av2sv

-------------------------------`(fi.)av2sv`-----------------------------------
Compute reflection coefficients sv from transfer-function denominator av.
#### Usage
```faust
sv = av2sv(av)
```
Where:
* `av`: parallel signal bank `a1,...,aN`
* `sv`: parallel signal bank `s1,...,sN`
where `ro = ith` reflection coefficient, and
`ai` = coefficient of `z^(-i)` in the filter
transfer-function denominator `A(z)`.
#### Test
```faust
fi = library("filters.lib");
si = library("signals.lib");
av2sv_test = fi.av2sv((-0.4, 0.1)) : si.bus(2);
```
#### References
<https://ccrma.stanford.edu/~jos/filters/Step_Down_Procedure.html>
(where reflection coefficients are denoted by k rather than s).

---

## fi.bvav2nuv

----------------------------`(fi.)bvav2nuv`--------------------------------
Compute lattice tap coefficients from transfer-function coefficients.
#### Usage
```faust
nuv = bvav2nuv(bv,av)
```
Where:
* `av`: parallel signal bank `a1,...,aN`
* `bv`: parallel signal bank `b0,b1,...,aN`
* `nuv`: parallel signal bank  `nu1,...,nuN`
where `nui` is the i'th tap coefficient,
`bi` is the coefficient of `z^(-i)` in the filter numerator,
`ai` is the coefficient of `z^(-i)` in the filter denominator
#### Test
```faust
fi = library("filters.lib");
si = library("signals.lib");
bvav2nuv_test = fi.bvav2nuv((0.1, 0.2, 0.3), (-0.4, 0.1)) : si.bus(3);
```

---

## fi.iir_lat2

--------------------`(fi.)iir_lat2`-----------------------
Two-multiply lattice IIR filter of arbitrary order.
#### Usage
```faust
_ : iir_lat2(bv,av) : _
```
Where:
* `bv`: transfer-function numerator
* `av`: transfer-function denominator (monic)
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
iir_lat2_test = os.osc(440) : fi.iir_lat2((0.1, 0.2, 0.3), (-0.4, 0.1));
```

---

## fi.allpassnt

-----------------------`(fi.)allpassnt`--------------------------
Two-multiply lattice allpass (nested order-1 direct-form-ii allpasses), with taps.
#### Usage
```faust
_ : allpassnt(n,sv) : si.bus(n+1)
```
Where:
* `n`: the order of the filter
* `sv`: the reflection coefficients (-1 1)
The first output is the n-th order allpass output,
while the remaining outputs are taps taken from the
input of each delay element from the input to the output.
See (fi.)allpassn for the single-output case.
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
si = library("signals.lib");
allpassnt_test = os.osc(440) : fi.allpassnt(2, (0.3, -0.2)) : si.bus(3);
```

---

## fi.iir_kl

--------------------`(fi.)iir_kl`-----------------------
Kelly-Lochbaum ladder IIR filter of arbitrary order.
#### Usage
```faust
_ : iir_kl(bv,av) : _
```
Where:
* `bv`: transfer-function numerator
* `av`: transfer-function denominator (monic)
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
iir_kl_test = os.osc(440) : fi.iir_kl((0.1, 0.2, 0.3), (-0.4, 0.1));
```

---

## fi.allpassnklt

-----------------------`(fi.)allpassnklt`--------------------------
Kelly-Lochbaum ladder allpass.
#### Usage:
```faust
_ : allpassnklt(n,sv) : _
```
Where:
* `n`: the order of the filter
* `sv`: the reflection coefficients (-1 1)
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
si = library("signals.lib");
allpassnklt_test = os.osc(440) : fi.allpassnklt(2, (0.3, -0.2)) : si.bus(3);
```

---

## fi.iir_lat1

--------------------`(fi.)iir_lat1`-----------------------
One-multiply lattice IIR filter of arbitrary order.
#### Usage
```faust
_ : iir_lat1(bv,av) : _
```
Where:
* bv: transfer-function numerator as a bank of parallel signals
* av: transfer-function denominator as a bank of parallel signals
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
iir_lat1_test = os.osc(440) : fi.iir_lat1((0.1, 0.2, 0.3), (-0.4, 0.1));
```

---

## fi.allpassn1mt

-----------------------`(fi.)allpassn1mt`--------------------------
One-multiply lattice allpass with tap lines.
#### Usage
```faust
_ : allpassn1mt(N,sv) : _
```
Where:
* `N`: the order of the filter (fixed at compile time)
* `sv`: the reflection coefficients (-1 1)
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
si = library("signals.lib");
allpassn1mt_test = os.osc(440) : fi.allpassn1mt(2, (0.3, -0.2)) : si.bus(3);
```

---

## fi.iir_nl

-------------------------------`(fi.)iir_nl`-------------------------
Normalized ladder filter of arbitrary order.
#### Usage
```faust
_ : iir_nl(bv,av) : _
```
Where:
* `bv`: transfer-function numerator
* `av`: transfer-function denominator (monic)
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
iir_nl_test = os.osc(440) : fi.iir_nl((0.1, 0.2, 0.3), (-0.4, 0.1));
```
#### References
* J. D. Markel and A. H. Gray, Linear Prediction of Speech, New York: Springer Verlag, 1976.
* <https://ccrma.stanford.edu/~jos/pasp/Normalized_Scattering_Junctions.html>

---

## fi.allpassnnlt

-------------------------------`(fi.)allpassnnlt`-------------------------
Normalized ladder allpass filter of arbitrary order.
#### Usage:
```faust
_ : allpassnnlt(N,sv) : _
```
Where:
* `N`: the order of the filter (fixed at compile time)
* `sv`: the reflection coefficients (-1 1)
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
si = library("signals.lib");
allpassnnlt_test = os.osc(440) : fi.allpassnnlt(2, (0.3, -0.2)) : si.bus(3);
```
#### References
* J. D. Markel and A. H. Gray, Linear Prediction of Speech, New York: Springer Verlag, 1976.
* <https://ccrma.stanford.edu/~jos/pasp/Normalized_Scattering_Junctions.html>

---

## fi.tf2np

--------------------------------`(fi.)tf2np`------------------------------------
Biquad based on a stable second-order Normalized Ladder Filter
(more robust to modulation than `tf2` and protected against instability).
#### Usage
```faust
_ : tf2np(b0,b1,b2,a1,a2) : _
```
Where:
* `b`: transfer-function numerator
* `a`: transfer-function denominator (monic)
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
tf2np_test = os.osc(440) : fi.tf2np(0.6, 0.3, 0.2, -0.5, 0.2);
```

---

## fi.wgr

-----------------------------`(fi.)wgr`---------------------------------
Second-order transformer-normalized digital waveguide resonator.
#### Usage
```faust
_ : wgr(f,r) : _
```
Where:
* `f`: resonance frequency (Hz)
* `r`: loss factor for exponential decay (set to 1 to make a numerically stable oscillator)
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
wgr_test = fi.wgr(440, 0.995, os.osc(440));
```
#### References
* <https://ccrma.stanford.edu/~jos/pasp/Power_Normalized_Waveguide_Filters.html>
* <https://ccrma.stanford.edu/~jos/pasp/Digital_Waveguide_Oscillator.html>

---

## fi.nlf2

-----------------------------`(fi.)nlf2`--------------------------------
Second order normalized digital waveguide resonator.
#### Usage
```faust
_ : nlf2(f,r) : _
```
Where:
* `f`: resonance frequency (Hz)
* `r`: loss factor for exponential decay (set to 1 to make a sinusoidal oscillator)
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
nlf2_test = fi.nlf2(440, 0.995, os.osc(440));
```
#### References
<https://ccrma.stanford.edu/~jos/pasp/Power_Normalized_Waveguide_Filters.html>

---

## fi.apnl

------------`(fi.)apnl`---------------
Passive Nonlinear Allpass based on Pierce switching springs idea.
Switch between allpass coefficient `a1` and `a2` at signal zero crossings.
#### Usage
```faust
_ : apnl(a1,a2) : _
```
Where:
* `a1` and `a2`: allpass coefficients
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
apnl_test = fi.apnl(0.5, -0.5, os.osc(440));
```
#### References
* "A Passive Nonlinear Digital Filter Design ..." by John R. Pierce and Scott
A. Van Duyne, JASA, vol. 101, no. 2, pp. 1120-1126, 1997

---

## fi.scatN

-----------------------`(fi.)scatN`--------------------------
N-port scattering junction.
#### Usage
```faust
si.bus(N) : scatN(N,av,filter) : si.bus(N)
```
Where:
* `N`: number of incoming/outgoing waves
* `av`: vector (list) of `N` alpha parameters (each between 0 and 2, and normally summing to 2): <https://ccrma.stanford.edu/~jos/pasp/Alpha_Parameters.html>
* `filter` : optional junction filter to apply (`_` for none, see below)
With no filter:
- The junction is _lossless_ when the alpha parameters sum to 2 ("allpass").
- The junction is _passive_ but lossy when the alpha parameters sum to less than 2 ("resistive loss").
- Dynamic and reactive junctions are obtained using the `filter` argument.
For guaranteed stability, the filter should be _positive real_. (See 2nd ref. below).
For \(N=2\) (two-port scattering), the reflection coefficient \(\rho\) corresponds
to alpha parameters \(1\pm\rho\).
#### Example: Whacky echo chamber made of 16 lossless "acoustic tubes":
```faust
process = _ : *(1.0/sqrt(N)) <: daisyRev(16,2,0.9999) :> _,_ with { 
daisyRev(N,Dp2,G) = si.bus(N) : (si.bus(2*N) :> si.bus(N)
: fi.scatN(N, par(i,N,2*G/float(N)), fi.lowpass(1,5000.0))
: par(i,N,de.delay(DS(i),DS(i)-1))) ~ si.bus(N) with { DS(i) = 2^(Dp2+i); };
};
```
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
scatN_test = (os.osc(440), os.osc(660)) : fi.scatN(2, (1, 1), _);
```
#### References
* <https://ccrma.stanford.edu/~jos/pasp/Loaded_Waveguide_Junctions.html>
* <https://ccrma.stanford.edu/~jos/pasp/Passive_String_Terminations.html>
* <https://ccrma.stanford.edu/~jos/pasp/Unloaded_Junctions_Alpha_Parameters.html>

---

## fi.scat

---------------`(fi.)scat`-----------------
Scatter off of reflectance r with reflection coefficient s.
#### Usage:
```faust
_ : scat(s,r) : _
```
#### Where:
* `s`: reflection coefficient between -1 and 1 for stability
* `r`: single-input, single-output block diagram,
having gain less than 1 at all frequencies for stability.
#### Example: the following program should produce all zeros:
```faust
process = fi.allpassn(3,(.3,.2,.1)), fi.scat(.1, fi.scat(.2, fi.scat(.3, _)))
:> - : ^(2) : +~_;
```
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
scat_test = os.osc(440) : fi.scat(0.5, _);
```
#### References
* <https://ccrma.stanford.edu/~jos/pasp/Scattering_Impedance_Changes.html>

---

## fi.allpassn

---------------`(fi.)allpassn`-----------------
Two-multiply lattice filter.
#### Usage:
```faust
_ : allpassn(n,sv) : _
```
#### Where:
* `n`: the order of the filter
* `sv`: the reflection coefficients (-1 1)
* `sv`: the reflection coefficients  (s1,s2,...,sN), each between -1 and 1.
Equivalent to `fi.allpassnt(n,sv) : _, par(i,n,!);`
Equivalent to `fi.scat( s(n), fi.scat( s(n-1), ..., fi.scat( s(1), _ )))
with { s(k) = ba.take(k,sv); } ;`
Identical to `allpassn` in `old/filter.lib`.
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
allpassn_test = os.osc(440) : fi.allpassn(3, (0.3, 0.2, 0.1));
```
#### References
* J. D. Markel and A. H. Gray: Linear Prediction of Speech, New York: Springer Verlag, 1976.
* <https://ccrma.stanford.edu/~jos/pasp/Conventional_Ladder_Filters.html>

---

## fi.allpassnn

---------------`(fi.)allpassnn`-----------------
Normalized form - four multiplies and two adds per section,
but coefficients can be time varying and nonlinear without
"parametric amplification" (modulation of signal energy).
#### Usage:
```faust
_ : allpassnn(n,tv) : _
```
Where:
* `n`: the order of the filter
* `tv`: the reflection coefficients (-PI PI)
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
allpassnn_test = os.osc(440) : fi.allpassnn(3, (0.3, 0.2, 0.1));
```
power-normalized (reflection coefficients s = sin(t)):

---

## fi.allpassnkl

---------------`(fi.)allpassnkl`-----------------
Kelly-Lochbaum form - four multiplies and two adds per
section, but all signals have an immediate physical
interpretation as traveling pressure waves, etc.
#### Usage:
```faust
_ : allpassnkl(n,sv) : _
```
Where:
* `n`: the order of the filter
* `sv`: the reflection coefficients (-1 1)
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
allpassnkl_test = os.osc(440) : fi.allpassnkl(3, (0.3, 0.2, 0.1));
```
Kelly-Lochbaum:

---

## fi.allpass1m

---------------`(fi.)allpass1m`-----------------
One-multiply form - one multiply and three adds per section.
Normally the most efficient in special-purpose hardware.
#### Usage:
```faust
_ : allpassn1m(n,sv) : _
```
Where:
* `n`: the order of the filter
* `sv`: the reflection coefficients (-1 1)
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
allpassn1m_test = os.osc(440) : fi.allpassn1m(3, (0.3, 0.2, 0.1));
```
one-multiply:

---

## fi.tf1snp

-----------------------------`(fi.)tf1snp`-------------------------------
First-order special case of tf2snp above.
#### Usage
```faust
_ : tf1snp(b1,b0,a0) : _
```
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
ma = library("maths.lib");
tf1snp_test = os.osc(440) : fi.tf1snp(0, 1, 1, ma.PI*ma.SR/2);
```

---

## fi.tf3slf

-----------------------------`(fi.)tf3slf`-------------------------------
Analogous to `tf2s` above, but third order, and using the typical
low-frequency-matching bilinear-transform constant 2/T ("lf" series)
instead of the specific-frequency-matching value used in `tf2s` and `tf1s`.
Note the lack of a "w1" argument.
#### Usage
```faust
_ : tf3slf(b3,b2,b1,b0,a3,a2,a1,a0) : _
```
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
tf3slf_test = os.osc(440) : fi.tf3slf(0, 0, 0, 1, 1, 2, 2, 1);
```

---

## fi.tf1s

-----------------------------`(fi.)tf1s`--------------------------------
First-order direct-form digital filter,
specified by ANALOG transfer-function polynomials B(s)/A(s),
and a frequency-scaling parameter.
#### Usage
```faust
_ : tf1s(b1,b0,a0,w1) : _
```
Where:
b1 s + b0
H(s) = ----------
s + a0
and `w1` is the desired digital frequency (in radians/second)
corresponding to analog frequency 1 rad/sec (i.e., `s = j`).
#### Example test program
A first-order ANALOG Butterworth lowpass filter,
normalized to have cutoff frequency at 1 rad/sec,
has transfer function:
1
H(s) = -------
s + 1
so `b0 = a0 = 1` and `b1 = 0`.  Therefore, a DIGITAL first-order
Butterworth lowpass with gain -3dB at `SR/4` is specified as
```faust
tf1s(0,1,1,PI*SR/2); // digital half-band order 1 Butterworth
```
#### Method
Bilinear transform scaled for exact mapping of w1.
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
ma = library("maths.lib");
tf1s_test = os.osc(440) : fi.tf1s(0, 1, 1, ma.PI*ma.SR/2);
```
#### References
* <https://ccrma.stanford.edu/~jos/pasp/Bilinear_Transformation.html>

---

## fi.tf2sb

-----------------------------`(fi.)tf2sb`--------------------------------
Bandpass mapping of `tf2s`: In addition to a frequency-scaling parameter
`w1` (set to HALF the desired passband width in rad/sec),
there is a desired center-frequency parameter wc (also in rad/s).
Thus, `tf2sb` implements a fourth-order digital bandpass filter section
specified by the coefficients of a second-order analog lowpass prototype
section.  Such sections can be combined in series for higher orders.
The order of mappings is (1) frequency scaling (to set lowpass cutoff w1),
(2) bandpass mapping to wc, then (3) the bilinear transform, with the
usual scale parameter `2*SR`.  Algebra carried out in maxima and pasted here.
#### Usage
```faust
_ : tf2sb(b2,b1,b0,a1,a0,w1,wc) : _
```
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
ma = library("maths.lib");
tf2sb_test = os.osc(440) : fi.tf2sb(0, 0, 1, sqrt(2), 1, 2*ma.PI*200, 2*ma.PI*1000);
```

---

## fi.tf1sb

-----------------------------`(fi.)tf1sb`--------------------------------
First-to-second-order lowpass-to-bandpass section mapping,
analogous to tf2sb above.
#### Usage
```faust
_ : tf1sb(b1,b0,a0,w1,wc) : _
```
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
ma = library("maths.lib");
tf1sb_test = os.osc(440) : fi.tf1sb(0, 1, 1, 2*ma.PI*200, 2*ma.PI*1000);
```

---

## fi.resonlp

------------------`(fi.)resonlp`-----------------
Simple resonant lowpass filter based on `tf2s` (virtual analog).
`resonlp` is a standard Faust function.
#### Usage
```faust
_ : resonlp(fc,Q,gain) : _
_ : resonhp(fc,Q,gain) : _
_ : resonbp(fc,Q,gain) : _

```
Where:
* `fc`: center frequency (Hz)
* `Q`: q
* `gain`: gain (0-1)
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
resonlp_test = os.osc(440) : fi.resonlp(1000, 2, 0.8);
```
resonlp = 2nd-order lowpass with corner resonance:

---

## fi.resonhp

------------------`(fi.)resonhp`-----------------
Simple resonant highpass filters based on `tf2s` (virtual analog).
`resonhp` is a standard Faust function.
#### Usage
```faust
_ : resonlp(fc,Q,gain) : _
_ : resonhp(fc,Q,gain) : _
_ : resonbp(fc,Q,gain) : _

```
Where:
* `fc`: center frequency (Hz)
* `Q`: q
* `gain`: gain (0-1)
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
resonhp_test = fi.resonhp(1000, 2, 0.8, os.osc(440));
```
resonhp = 2nd-order highpass with corner resonance:

---

## fi.resonbp

------------------`(fi.)resonbp`-----------------
Simple resonant bandpass filters based on `tf2s` (virtual analog).
`resonbp` is a standard Faust function.
#### Usage
```faust
_ : resonlp(fc,Q,gain) : _
_ : resonhp(fc,Q,gain) : _
_ : resonbp(fc,Q,gain) : _

```
Where:
* `fc`: center frequency (Hz)
* `Q`: q
* `gain`: gain (0-1)
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
resonbp_test = os.osc(440) : fi.resonbp(1000, 2, 0.8);
```
resonbp = 2nd-order bandpass

---

## fi.lowpass

----------------`(fi.)lowpass`--------------------
Nth-order Butterworth lowpass filter.
`lowpass` is a standard Faust function.
#### Usage
```faust
_ : lowpass(N,fc) : _
```
Where:
* `N`: filter order (number of poles), nonnegative constant numerical expression
* `fc`: desired cut-off frequency (-3dB frequency) in Hz
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
lowpass_test = os.osc(440) : fi.lowpass(4, 2000);
```
#### References
* <https://ccrma.stanford.edu/~jos/filters/Butterworth_Lowpass_Design.html>
* `butter` function in Octave `("[z,p,g] = butter(N,1,'s');")`

---

## fi.highpass

----------------`(fi.)highpass`--------------------
Nth-order Butterworth highpass filter.
`highpass` is a standard Faust function.
#### Usage
```faust
_ : highpass(N,fc) : _
```
Where:
* `N`: filter order (number of poles), nonnegative constant numerical expression
* `fc`: desired cut-off frequency (-3dB frequency) in Hz
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
highpass_test = os.osc(440) : fi.highpass(4, 500);
```
#### References
* <https://ccrma.stanford.edu/~jos/filters/Butterworth_Lowpass_Design.html>
* `butter` function in Octave `("[z,p,g] = butter(N,1,'s');")`

---

## fi.lowpass0_highpass1

-------------`(fi.)lowpass0_highpass1`--------------
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
lowpass0_highpass1_test = os.osc(440) : fi.lowpass0_highpass1(0, 2, 1000);
```

---

## fi.highpass_plus_lowpass

--------------------`(fi.)highpass_plus_lowpass`----------------
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
highpass_plus_lowpass_test = os.osc(440) : fi.highpass_plus_lowpass(3, 1000);
```

---

## fi.highpass_minus_lowpass

--------------------`(fi.)highpass_minus_lowpass`----------------
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
highpass_minus_lowpass_test = os.osc(440) : fi.highpass_minus_lowpass(3, 1000);
```

---

## fi.highpass_plus_lowpass_even

--------------------`(fi.)highpass_plus_lowpass_even`----------------
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
highpass_plus_lowpass_even_test = os.osc(440) : fi.highpass_plus_lowpass_even(4, 1000);
```

---

## fi.highpass_plus_lowpass_even

--------------------`(fi.)highpass_plus_lowpass_even`----------------
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
highpass_minus_lowpass_even_test = os.osc(440) : fi.highpass_minus_lowpass_even(4, 1000);
```

---

## fi.highpass_minus_lowpass_odd

--------------------`(fi.)highpass_minus_lowpass_odd`----------------
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
highpass_plus_lowpass_odd_test = os.osc(440) : fi.highpass_plus_lowpass_odd(3, 1000);
```
FIXME: Rewrite the following, as for orders 3 and 5 above,
to eliminate pole-zero cancellations:

---

## fi.highpass_minus_lowpass_odd

--------------------`(fi.)highpass_minus_lowpass_odd`----------------
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
highpass_minus_lowpass_odd_test = os.osc(440) : fi.highpass_minus_lowpass_odd(3, 1000);
```
FIXME: Rewrite the following, as for orders 3 and 5 above,
to eliminate pole-zero cancellations/

---

## fi.lowpass3e

-----------------------------`(fi.)lowpass3e`-----------------------------
Third-order Elliptic (Cauer) lowpass filter.
#### Usage
```faust
_ : lowpass3e(fc) : _
```
Where:
* `fc`: -3dB frequency in Hz
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
lowpass3e_test = os.osc(440) : fi.lowpass3e(1000);
```
#### Design
For spectral band-slice level display (see `octave_analyzer3e`):
```faust
[z,p,g] = ncauer(Rp,Rs,3);  % analog zeros, poles, and gain, where
Rp = 60  % dB ripple in stopband
Rs = 0.2 % dB ripple in passband
```

---

## fi.lowpass6e

-----------------------------`(fi.)lowpass6e`-----------------------------
Sixth-order Elliptic/Cauer lowpass filter.
#### Usage
```faust
_ : lowpass6e(fc) : _
```
Where:
* `fc`: -3dB frequency in Hz
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
lowpass6e_test = os.osc(440) : fi.lowpass6e(1000);
```
#### Design
For spectral band-slice level display (see octave_analyzer6e):
```faust
[z,p,g] = ncauer(Rp,Rs,6);  % analog zeros, poles, and gain, where
Rp = 80  % dB ripple in stopband
Rs = 0.2 % dB ripple in passband
```

---

## fi.highpass3e

-----------------------------`(fi.)highpass3e`-----------------------------
Third-order Elliptic (Cauer) highpass filter. Inversion of `lowpass3e` wrt unit
circle in s plane (s <- 1/s).
#### Usage
```faust
_ : highpass3e(fc) : _
```
Where:
* `fc`: -3dB frequency in Hz
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
highpass3e_test = os.osc(440) : fi.highpass3e(1000);
```

---

## fi.highpass6e

-----------------------------`(fi.)highpass6e`-----------------------------
Sixth-order Elliptic/Cauer highpass filter. Inversion of `lowpass3e` wrt unit
circle in s plane (s <- 1/s).
#### Usage
```faust
_ : highpass6e(fc) : _
```
Where:
* `fc`: -3dB frequency in Hz
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
highpass6e_test = os.osc(440) : fi.highpass6e(1000);
```

---

## fi.bandpass

--------------------`(fi.)bandpass`----------------
Order 2*Nh Butterworth bandpass filter made using the transformation
`s <- s + wc^2/s` on `lowpass(Nh)`, where `wc` is the desired bandpass center
frequency.  The `lowpass(Nh)` cutoff `w1` is half the desired bandpass width.
`bandpass` is a standard Faust function.
#### Usage
```faust
_ : bandpass(Nh,fl,fu) : _
```
Where:
* `Nh`: HALF the desired bandpass order (which is therefore even)
* `fl`: lower -3dB frequency in Hz
* `fu`: upper -3dB frequency in Hz
Thus, the passband width is `fu-fl`,
and its center frequency is `(fl+fu)/2`.
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
bandpass_test = os.osc(440) : fi.bandpass(2, 500, 1500);
```

---

## fi.bandstop

--------------------`(fi.)bandstop`----------------
Order 2*Nh Butterworth bandstop filter made using the transformation
`s <- s + wc^2/s` on `highpass(Nh)`, where `wc` is the desired bandpass center
frequency.  The `highpass(Nh)` cutoff `w1` is half the desired bandpass width.
`bandstop` is a standard Faust function.
#### Usage
```faust
_ : bandstop(Nh,fl,fu) : _
```
Where:
* `Nh`: HALF the desired bandstop order (which is therefore even)
* `fl`: lower -3dB frequency in Hz
* `fu`: upper -3dB frequency in Hz
Thus, the passband (stopband) width is `fu-fl`,
and its center frequency is `(fl+fu)/2`.
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
bandstop_test = os.osc(440) : fi.bandstop(2, 500, 1500);
```

---

## fi.bandstop

--------------------`(fi.)bandstop`----------------
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
bandpass0_bandstop1_test = os.osc(440) : fi.bandpass0_bandstop1(0, 2, 500, 1500);
```

---

## fi.bandpass6e

---------------------`(fi.)bandpass6e`-----------------------------
Order 12 elliptic bandpass filter analogous to `bandpass(6)`.

---

## fi.bandpass12e

----------------------`(fi.)bandpass12e`---------------------------
Order 24 elliptic bandpass filter analogous to `bandpass(6)`.

---

## fi.pospass

------------------------`(fi.)pospass`---------------------------
Positive-Pass Filter (single-side-band filter).
#### Usage
```faust
_ : pospass(N,fc) : _,_
```
where
* `N`: filter order (Butterworth bandpass for positive frequencies).
* `fc`: lower bandpass cutoff frequency in Hz.
- Highpass cutoff frequency at ma.SR/2 - fc Hz.
#### Example test program
* See `dm.pospass_demo`
* Look at frequency response
#### Method
A filter passing only positive frequencies can be made from a
half-band lowpass by modulating it up to the positive-frequency range.
Equivalently, down-modulate the input signal using a complex sinusoid at -SR/4 Hz,
lowpass it with a half-band filter, and modulate back up by SR/4 Hz.
In Faust/math notation:
$$pospass(N) = \ast(e^{-j\frac{\pi}{2}n}) : \mbox{lowpass(N,SR/4)} : \ast(e^{j\frac{\pi}{2}n})$$
An approximation to the Hilbert transform is given by the
imaginary output signal:
```faust
hilbert(N) = pospass(N) : !,*(2);
```
#### References
* <https://ccrma.stanford.edu/~jos/mdft/Analytic_Signals_Hilbert_Transform.html>
* <https://ccrma.stanford.edu/~jos/sasp/Comparison_Optimal_Chebyshev_FIR_I.html>
* <https://ccrma.stanford.edu/~jos/sasp/Hilbert_Transform.html>

---

## fi.lowshelf

----------------------`(fi.)lowshelf`----------------------
First-order "low shelf" filter (gain boost|cut between dc and some frequency)
`low_shelf` is a standard Faust function.
#### Usage
```faust
_ : lowshelf(N,L0,fx) : _
_ : low_shelf(L0,fx) : _ // default case (order 3)
_ : lowshelf_other_freq(N,L0,fx) : _
```
Where:
* `N`: filter order 1, 3, 5, ... (odd only, default should be 3, a constant numerical expression)
* `L0`: desired level (dB) between dc and fx (boost `L0>0` or cut `L0<0`)
* `fx`: -3dB frequency of lowpass band (`L0>0`) or upper band (`L0<0`)
(see "SHELF SHAPE" below).
The gain at SR/2 is constrained to be 1.
The generalization to arbitrary odd orders is based on the well known
fact that odd-order Butterworth band-splits are allpass-complementary
(see filterbank documentation below for references).
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
lowshelf_test = os.osc(440) : fi.lowshelf(3, 6, 500);
```
#### Shelf Shape
The magnitude frequency response is approximately piecewise-linear
on a log-log plot ("BODE PLOT").  The Bode "stick diagram" approximation
L(lf) is easy to state in dB versus dB-frequency lf = dB(f):
* L0 > 0:
* L(lf) = L0, f between 0 and fx = 1st corner frequency;
* L(lf) = L0 - N * (lf - lfx), f between fx and f2 = 2nd corner frequency;
* L(lf) = 0, lf > lf2.
* lf2 = lfx + L0/N = dB-frequency at which level gets back to 0 dB.
* L0 < 0:
* L(lf) = L0, f between 0 and f1 = 1st corner frequency;
* L(lf) = - N * (lfx - lf), f between f1 and lfx = 2nd corner frequency;
* L(lf) = 0, lf > lfx.
* lf1 = lfx + L0/N = dB-frequency at which level goes up from L0.
See `lowshelf_other_freq`.
#### References
* See "Parametric Equalizers" above for references regarding `low_shelf`, `high_shelf`, and `peak_eq`.

---

## fi.low_shelf

----------------------`(fi.)low_shelf`----------------------
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
low_shelf_test = os.osc(440) : fi.low_shelf(6, 500);
```

---

## fi.low_shelf1_l

----------------------`(fi.)low_shelf1_l`----------------------
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
low_shelf1_l_test = fi.low_shelf1_l(2, 500, os.osc(440));
```

---

## fi.low_shelf1_l

----------------------`(fi.)low_shelf1_l`----------------------
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
low_shelf1_l_test = fi.low_shelf1_l(2, 500, os.osc(440));
```

---

## fi.lowshelf_other_freq

----------------------`(fi.)lowshelf_other_freq`----------------------
#### Test
```faust
fi = library("filters.lib");
lowshelf_other_freq_test = fi.lowshelf_other_freq(3, 6, 500);
```

---

## fi.high_shelf

-------------`(fi.)high_shelf`--------------
First-order "high shelf" filter (gain boost|cut above some frequency).
`high_shelf` is a standard Faust function.
#### Usage
```faust
_ : highshelf(N,Lpi,fx) : _
_ : high_shelf(L0,fx) : _ // default case (order 3)
_ : highshelf_other_freq(N,Lpi,fx) : _
```
Where:
* `N`: filter order 1, 3, 5, ... (odd only, a constant numerical expression).
* `Lpi`: desired level (dB) between fx and SR/2 (boost Lpi>0 or cut Lpi<0)
* `fx`: -3dB frequency of highpass band (L0>0) or lower band (L0<0)
(Use highshelf_other_freq() below to find the other one.)
The gain at dc is constrained to be 1.
See `lowshelf` documentation above for more details on shelf shape.
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
highshelf_test = os.osc(440) : fi.highshelf(3, 6, 2000);
```
#### References
* See "Parametric Equalizers" above for references regarding `low_shelf`, `high_shelf`, and `peak_eq`.

---

## fi.high_shelf

----------------------`(fi.)high_shelf`----------------------
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
high_shelf_test = os.osc(440) : fi.high_shelf(6, 2000);
```

---

## fi.high_shelf1

----------------------`(fi.)high_shelf1`----------------------
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
high_shelf1_test = fi.high_shelf1(6, 2000, os.osc(440));
```

---

## fi.high_shelf1_l

----------------------`(fi.)high_shelf1_l`----------------------
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
high_shelf1_l_test = fi.high_shelf1_l(2, 2000, os.osc(440));
```

---

## fi.highshelf_other_freq

----------------------`(fi.)highshelf_other_freq`----------------------
#### Test
```faust
fi = library("filters.lib");
highshelf_other_freq_test = fi.highshelf_other_freq(3, 6, 2000);
```

---

## fi.peak_eq

-------------------`(fi.)peak_eq`------------------------------
Second order "peaking equalizer" section (gain boost or cut near some frequency)
Also called a "parametric equalizer" section.
`peak_eq` is a standard Faust function.
#### Usage
```faust
_ : peak_eq(Lfx,fx,B) : _
```
Where:
* `Lfx`: level (dB) at fx (boost Lfx>0 or cut Lfx<0)
* `fx`: peak frequency (Hz)
* `B`: bandwidth (B) of peak in Hz
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
peak_eq_test = os.osc(440) : fi.peak_eq(6, 1000, 200);
```
#### References
* See "Parametric Equalizers" above for references regarding `low_shelf`, `high_shelf`, and `peak_eq`.

---

## fi.peak_eq_cq

--------------------`(fi.)peak_eq_cq`----------------------------
Constant-Q second order peaking equalizer section.
#### Usage
```faust
_ : peak_eq_cq(Lfx,fx,Q) : _
```
Where:
* `Lfx`: level (dB) at fx
* `fx`: boost or cut frequency (Hz)
* `Q`: "Quality factor" = fx/B where B = bandwidth of peak in Hz
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
peak_eq_cq_test = os.osc(440) : fi.peak_eq_cq(6, 1000, 4);
```
#### References
* See "Parametric Equalizers" above for references regarding `low_shelf`, `high_shelf`, and `peak_eq`.

---

## fi.peak_eq_rm

-------------------`(fi.)peak_eq_rm`--------------------------
Regalia-Mitra second order peaking equalizer section.
#### Usage
```faust
_ : peak_eq_rm(Lfx,fx,tanPiBT) : _
```
Where:
* `Lfx`: level (dB) at fx
* `fx`: boost or cut frequency (Hz)
* `tanPiBT`: `tan(PI*B/SR)`, where B = -3dB bandwidth (Hz) when 10^(Lfx/20) = 0
~ PI*B/SR for narrow bandwidths B
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
ma = library("maths.lib");
peak_eq_rm_test = os.osc(440) : fi.peak_eq_rm(6, 1000, ma.tan(ma.PI*200/ma.SR));
```
#### References
P.A. Regalia, S.K. Mitra, and P.P. Vaidyanathan,
"The Digital All-Pass Filter: A Versatile Signal Processing Building Block"
Proceedings of the IEEE, 76(1):19-37, Jan. 1988.  (See pp. 29-30.)
See also "Parametric Equalizers" above for references on shelf
and peaking equalizers in general.

---

## fi.spectral_tilt

---------------------`(fi.)spectral_tilt`-------------------------
Spectral tilt filter, providing an arbitrary spectral rolloff factor
alpha in (-1,1), where
-1 corresponds to one pole (-6 dB per octave), and
+1 corresponds to one zero (+6 dB per octave).
In other words, alpha is the slope of the ln magnitude versus ln frequency.
For a "pinking filter" (e.g., to generate 1/f noise from white noise),
set alpha to -1/2.
#### Usage
```faust
_ : spectral_tilt(N,f0,bw,alpha) : _
```
Where:
* `N`: desired integer filter order (fixed at compile time)
* `f0`: lower frequency limit for desired roll-off band > 0
* `bw`: bandwidth of desired roll-off band
* `alpha`: slope of roll-off desired in nepers per neper,
between -1 and 1 (ln mag / ln radian freq)
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
spectral_tilt_test = os.osc(440) : fi.spectral_tilt(4, 200, 2000, -0.5);
```
#### Example test program
See `dm.spectral_tilt_demo` and the documentation for `no.pink_noise`.
#### References
J.O. Smith and H.F. Smith,
"Closed Form Fractional Integration and Differentiation via Real Exponentially Spaced Pole-Zero Pairs",
arXiv.org publication arXiv:1606.06154 [cs.CE], June 7, 2016, <http://arxiv.org/abs/1606.06154>

---

## fi.levelfilter

----------------------`(fi.)levelfilter`----------------------
Dynamic level lowpass filter.
`levelfilter` is a standard Faust function.
#### Usage
```faust
_ : levelfilter(L,freq) : _
```
Where:
* `L`: desired level (in dB) at Nyquist limit (SR/2), e.g., -60
* `freq`: corner frequency (-3dB point) usually set to fundamental freq
* `N`: Number of filters in series where L = L/N
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
levelfilter_test = fi.levelfilter(0.1, 200, os.osc(440));
```
#### References
* <https://ccrma.stanford.edu/realsimple/faust_strings/Dynamic_Level_Lowpass_Filter.html>

---

## fi.levelfilterN

----------------------`(fi.)levelfilterN`----------------------
Dynamic level lowpass filter.
#### Usage
```faust
_ : levelfilterN(N,freq,L) : _
```
Where:
* `N`: Number of filters in series where L = L/N, a constant numerical expression
* `freq`: corner frequency (-3dB point) usually set to fundamental freq
* `L`: desired level (in dB) at Nyquist limit (SR/2), e.g., -60
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
levelfilterN_test = os.osc(440) : fi.levelfilterN(3, 200, 0.1);
```
#### References
* <https://ccrma.stanford.edu/realsimple/faust_strings/Dynamic_Level_Lowpass_Filter.html>

---

## fi.mth_octave_filterbank_alt

------------------------`(fi.)mth_octave_filterbank_alt`-------------------------
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
mth_octave_filterbank_alt_test = os.osc(440) : fi.mth_octave_filterbank_alt(3, 2, 8000, 2);
```

---

## fi.mth_octave_filterbank3

------------------------`(fi.)mth_octave_filterbank3`-------------------------
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
mth_octave_filterbank3_test = os.osc(440) : fi.mth_octave_filterbank3(2, 8000, 2);
```

---

## fi.mth_octave_filterbank5

------------------------`(fi.)mth_octave_filterbank5`-------------------------
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
mth_octave_filterbank5_test = os.osc(440) : fi.mth_octave_filterbank5(2, 8000, 2);
```

---

## fi.mth_octave_filterbank_default

------------------------`(fi.)mth_octave_filterbank_default`-------------------------
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
mth_octave_filterbank_default_test = os.osc(440) : fi.mth_octave_filterbank_default(2, 8000, 2);
```

---

## fi.filterbank

---------------`(fi.)filterbank`--------------------------
Filter bank.
`filterbank` is a standard Faust function.
#### Usage
```faust
_ : filterbank (O,freqs) : par(i,N,_) // Butterworth band-splits
```
Where:
* `O`: band-split filter order (odd integer required for filterbank[i], a constant numerical expression)
* `freqs`: (fc1,fc2,...,fcNs) [in numerically ascending order], where
Ns=N-1 is the number of octave band-splits
(total number of bands N=Ns+1).
If frequencies are listed explicitly as arguments, enclose them in parens:
```faust
_ : filterbank(3,(fc1,fc2)) : _,_,_
```
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
filterbank_test = os.osc(440) : fi.filterbank(3, (500, 2000));
```

---

## fi.filterbanki

-----------------`(fi.)filterbanki`----------------------
Inverted-dc filter bank.
#### Usage
```faust
_ : filterbanki(O,freqs) : par(i,N,_) // Inverted-dc version
```
Where:
* `O`: band-split filter order (odd integer required for `filterbank[i]`, a constant numerical expression)
* `freqs`: (fc1,fc2,...,fcNs) [in numerically ascending order], where
Ns=N-1 is the number of octave band-splits
(total number of bands N=Ns+1).
If frequencies are listed explicitly as arguments, enclose them in parens:
```faust
_ : filterbanki(3,(fc1,fc2)) : _,_,_
```
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
filterbanki_test = os.osc(440) : fi.filterbanki(3, (500, 2000));
```

---

## fi.svf

-----------------`(fi.)svf`----------------------
An environment with `lp`, `bp`, `hp`, `notch`, `peak`, `ap`, `bell`, `ls`, `hs` SVF based filters.
All filters have `freq` and `Q` parameters, the `bell`, `ls`, `hs` ones also have a `gain` third parameter.
#### Usage
```faust
_ : svf.xx(freq, Q, [gain]) : _
```
Where:
* `freq`: cut frequency
* `Q`: quality factor
* `[gain]`: gain in dB
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
svf_lp_test = fi.svf.lp(1000, 0.707, os.osc(440));
svf_bp_test = fi.svf.bp(1000, 0.707, os.osc(440));
svf_hp_test = fi.svf.hp(1000, 0.707, os.osc(440));
svf_notch_test = fi.svf.notch(1000, 0.707, os.osc(440));
svf_peak_test = fi.svf.peak(1000, 0.707, os.osc(440));
svf_ap_test = fi.svf.ap(1000, 0.707, os.osc(440));
svf_bell_test = fi.svf.bell(1000, 0.707, 6, os.osc(440));
svf_ls_test = fi.svf.ls(500, 0.707, 6, os.osc(440));
svf_hs_test = fi.svf.hs(3000, 0.707, 6, os.osc(440));
```

---

## fi.svf_morph

-----------------`(fi.)svf_morph`--------------------
An SVF-based filter that can smoothly morph between
being lowpass, bandpass, and highpass.
#### Usage
```faust
_ : svf_morph(freq, Q, blend) : _
```
Where:
* `freq`: cutoff frequency
* `Q`: quality factor
* `blend`: [0..2] continuous, where 0 is `lowpass`, 1 is `bandpass`, and 2 is `highpass`. For performance, the value is not clamped to [0..2].
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
svf_morph_test = fi.svf_morph(1000, 0.707, 1, os.osc(440));
```
#### Example test program
```faust
process = no.noise : svf_morph(freq, q, blend)
with {
blend = hslider("Blend", 0, 0, 2, .01) : si.smoo;
q = hslider("Q", 1, 0.1, 10, .01) : si.smoo;
freq = hslider("freq", 5000, 100, 18000, 1) : si.smoo;
};
```
#### References
<https://github.com/mtytel/vital/blob/636ca0ef517a4db087a6a08a6a8a5e704e21f836/src/synthesis/filters/digital_svf.cpp#L292-L295>

---

## fi.svf_notch_morph

-----------------`(fi.)svf_notch_morph`--------------------
An SVF-based notch-filter that can smoothly morph between
being lowpass, notch, and highpass.
#### Usage
```faust
_ : svf_notch_morph(freq, Q, blend) : _
```
Where:
* `freq`: cutoff frequency
* `Q`: quality factor
* `blend`: [0..2] continuous, where 0 is `lowpass`, 1 is `notch`, and 2 is `highpass`. For performance, the value is not clamped to [0..2].
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
svf_notch_morph_test = fi.svf_notch_morph(1000, 0.707, 1, os.osc(440));
```
#### Example test program
```faust
process = no.noise : svf_notch_morph(freq, q, blend)
with {
blend = hslider("Blend", 0, 0, 2, .01) : si.smoo;
q = hslider("Q", 1, 0.1, 10, .01) : si.smoo;
freq = hslider("freq", 5000, 100, 18000, 1) : si.smoo;
};
```
#### References
<https://github.com/mtytel/vital/blob/636ca0ef517a4db087a6a08a6a8a5e704e21f836/src/synthesis/filters/digital_svf.cpp#L256C36-L263>

---

## fi.SVFTPT

----------`(fi.)SVFTPT`---------------------------------------------------------
Topology-preserving transform implementation following Zavalishin's method.
Outputs: lowpass, highpass, bandpass, normalised bandpass, notch, allpass,
peaking.
Each individual output can be recalled with its name in the environment as in:
`SVFTPT.LP2(1000.0, .707)`.
The 7 outputs can be recalled by using `SVF` name as in:
`SVFTPT.SVF(1000.0, .707)`.
Even though the implementation is different, the characteristics of this
filter are comparable to those of the `svf` environment in this library.
#### Usage:
```faust
_ : SVFTPT.xxx(CF, Q) : _
```
Where:
* `xxx` can be one of the following: `LP2`, `HP2`, `BP2`, `BP2Norm`, `Notch2`, `AP2`, `Peaking2`
* `CF`: cutoff in Hz
* `Q`: resonance
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
SVFTPT_SVF_test = fi.SVFTPT.SVF(1000, 0.707, os.osc(440));
SVFTPT_LP2_test = fi.SVFTPT.LP2(1000, 0.707, os.osc(440));
SVFTPT_HP2_test = fi.SVFTPT.HP2(1000, 0.707, os.osc(440));
SVFTPT_BP2_test = fi.SVFTPT.BP2(1000, 0.707, os.osc(440));
SVFTPT_BP2Norm_test = fi.SVFTPT.BP2Norm(1000, 0.707, os.osc(440));
SVFTPT_Notch2_test = fi.SVFTPT.Notch2(1000, 0.707, os.osc(440));
SVFTPT_AP2_test = fi.SVFTPT.AP2(1000, 0.707, os.osc(440));
SVFTPT_Peaking2_test = fi.SVFTPT.Peaking2(1000, 0.707, os.osc(440));
```

---

## fi.dynamicSmoothing

----------`(fi.)dynamicSmoothing`------------------------------------------------
Adaptive smoother based on Andy Simper's paper.
This filter uses both the lowpass and bandpass outputs of a
state-variable filter. The lowpass is used to smooth out the input signal,
the bandpass, which is a smoothed out version of the highpass, provides
information on the rate of change of the input. Hence, the bandpass signal
can be used to adjust the cutoff of the filter to quickly follow the input's
fast and large variations while effectively filtering out local
perturbations.
This implementation does not use an approximation for the CF computation,
and it deploys guards to prevent overshooting with extreme sensitivity
values.
#### Usage:
```faust
_ : dynamicSmoothing(sensitivity, baseCF) : _
```
Where:
* `sensitivity`: sensitivity to changes in the input signal.
The range is, theoretically, from 0 to INF, though anything between
0.0 and 1.0 should be reasonable
* `baseCF`: cutoff frequency, in Hz, when there is no variation in the
input signal
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
dynamicSmoothing_test = fi.dynamicSmoothing(0.5, 500, os.osc(440));
```
#### References
* <https://cytomic.com/files/dsp/DynamicSmoothing.pdf>

---

## fi.oneEuro

-----------------`(fi.)oneEuro`----------------------------------
The One Euro Filter (1€ Filter) is an adaptive lowpass filter.
This kind of filter is commonly used in object-tracking,
not necessarily audio processing.
#### Usage
```faust
_ : oneEuro(derivativeCutoff, beta, minCutoff) : _
```
Where:
* `derivativeCutoff`: Used to filter the first derivative of the input. 1 Hz is a good default.
* `beta`: "Speed" parameter where higher values reduce latency.
* `minCutoff`: Minimum cutoff frequency in Hz. Lower values remove more jitter.
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
oneEuro_test = os.osc(440) : fi.oneEuro(1, 0.5, 5);
```
#### References
* <https://gery.casiez.net/1euro/>

---

## fi.lowpassLR4

----------`(fi.)lowpassLR4`---------------------------------------------------
4th-order Linkwitz-Riley lowpass.
#### Usage
```faust
_ : lowpassLR4(cf) : _
```
Where:
* `cf` is the lowpass cutoff in Hz
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
lowpassLR4_test = os.osc(440) : fi.lowpassLR4(1000);
```

---

## fi.highpassLR4

----------`(fi.)highpassLR4`--------------------------------------------------
4th-order Linkwitz-Riley highpass.
#### Usage
```faust
_ : highpassLR4(cf) : _
```
Where:
* `cf` is the highpass cutoff in Hz
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
highpassLR4_test = os.osc(440) : fi.highpassLR4(1000);
```

---

## fi.crossover2LR4

----------`(fi.)crossover2LR4`------------------------------------------------
Two-way 4th-order Linkwitz-Riley crossover.
#### Usage
```faust
_ : crossover2LR4(cf) : si.bus(2)
```
Where:
* `cf` is the crossover split cutoff in Hz
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
crossover2LR4_test = os.osc(440) : fi.crossover2LR4(1000);
```

---

## fi.crossover3LR4

----------`(fi.)crossover3LR4`------------------------------------------------
Three-way 4th-order Linkwitz-Riley crossover.
#### Usage
```faust
_ : crossover3LR4(cf1, cf2) : si.bus(3)
```
Where:
* `cf1` is the crossover lower split cutoff in Hz
* `cf2` is the crossover upper split cutoff in Hz
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
crossover3LR4_test = os.osc(440) : fi.crossover3LR4(500, 2000);
```

---

## fi.crossover4LR4

----------`(fi.)crossover4LR4`------------------------------------------------
Four-way 4th-order Linkwitz-Riley crossover.
#### Usage
```faust
_ : crossover4LR4(cf1, cf2, cf3) : si.bus(4)
```
Where:
* `cf1` is the crossover lower split cutoff in Hz
* `cf2` is the crossover mid split cutoff in Hz
* `cf3` is the crossover upper split cutoff in Hz
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
crossover4LR4_test = os.osc(440) : fi.crossover4LR4(300, 1000, 3000);
```

---

## fi.crossover8LR4

----------`(fi.)crossover8LR4`------------------------------------------------
Eight-way 4th-order Linkwitz-Riley crossover.
#### Usage
```faust
_ : crossover8LR4(cf1, cf2, cf3, cf4, cf5, cf6, cf7) : si.bus(8)
```
Where:
* `cf1-cf7` are the crossover cutoff frequencies in Hz
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
crossover8LR4_test = os.osc(440) : fi.crossover8LR4(100, 200, 400, 800, 1600, 3200, 6400);
```

---

## fi.itu_r_bs_1770_4_kfilter

----------------------`(fi.)itu_r_bs_1770_4_kfilter`-------------------------
The prefilter from Recommendation ITU-R BS.1770-4 for loudness
measurement. Also known as "K-filter". The recommendation defines
biquad filter coefficients for a fixed sample rate of 48kHz (page
4-5). Here, we construct biquads for arbitrary samplerates.  The
resulting filter is normalized, such that the magnitude at 997Hz is
unity gain 1.0.
Please note, the ITU-recommendation handles the normalization in
equation (2) by subtracting 0.691dB, which is not needed with
`itu_r_bs_1770_4_kfilter`.
One option for future improvement might be, to round those filter
coefficients, that are almost equal to one. Second, the maximum
magnitude difference at 48kHz between the ITU-defined filter and
`itu_r_bs_1770_4_kfilter` is 0.001dB, which obviously could be
less.
#### Usage
```faust
_ : itu_r_bs_1770_4_kfilter : _
```
#### Test
```faust
fi = library("filters.lib");
os = library("oscillators.lib");
itu_r_bs_1770_4_kfilter_test = os.osc(440) : fi.itu_r_bs_1770_4_kfilter;
```
#### References
* <https://www.itu.int/rec/R-REC-BS.1770>
* <https://gist.github.com/jkbd/07521a98f7873a2dc3dbe16417930791>

---

## fi.avg_rect

----------------------------`(fi.)avg_rect`----------------------------------
Moving average.
#### Usage
```faust
_ : avg_rect(period) : _
```
Where:
* `period` is the averaging frame in seconds

---

## fi.avg_tau

----------------------------`(fi.)avg_tau`-------------------------------------
Averaging function based on a one-pole filter and the tau response time.
Tau represents the effective length of the one-pole impulse response,
that is, tau is the integral of the filter's impulse response. This
response is slower to reach the final value but has less ripples in
non-steady signals.
#### Usage
```faust
_ : avg_tau(period) : _
```
Where:
* `period` is the time, in seconds, for the system to decay by 1/e,
or to reach 1-1/e of its final value.
#### References
* <https://ccrma.stanford.edu/~jos/mdft/Exponentials.html>

---

## fi.avg_t60

----------------------------`(fi.)avg_t60`-------------------------------------
Averaging function based on a one-pole filter and the t60 response time.
This response is particularly useful when the system is required to
reach the final value after about `period` seconds.
#### Usage
```faust
_ : avg_t60(period) : _
```
Where:
* `period` is the time, in seconds, for the system to decay by 1/1000,
or to reach 1-1/1000 of its final value.
#### References
* <https://ccrma.stanford.edu/~jos/mdft/Audio_Decay_Time_T60.html>

---

## fi.avg_t19

----------------------------`(fi.)avg_t19`-------------------------------------
Averaging function based on a one-pole filter and the t19 response time.
This response is close to the moving-average algorithm as it roughly reaches
the final value after `period` seconds and shows about the same
oscillations for non-steady signals.
#### Usage
```faust
_ : avg_t19(period) : _
```
Where:
* `period` is the time, in seconds, for the system to decay by 1/e^2.2,
or to reach 1-1/e^2.2 of its final value.
#### References
Zölzer, U. (2008). Digital audio signal processing (Vol. 9). New York: Wiley.

---

## fi.kalman

-----------`(fi.)kalman`----------------------------------------------------
The Kalman filter. It returns the state (a bus of size `N`).
Note that the only compile-time constant arguments are `N` and `M`.
Other arguments are capitalized because they're matrices, and it makes
reading them much easier.
#### Usage
```faust
kalman(N, M, B, R, H, Q, F, reset, u, z) : si.bus(N)
```
Where:
* `N`: State size (constant int)
* `M`: Measurement size (constant int)
* `B`: Control input matrix (NxM)
* `R`: Measurement noise covariance matrix (MxM)
* `H`: Observation matrix (MxN)
* `Q`: Process noise covariance matrix (NxN)
* `F`: State transition matrix (NxN)
* `reset`: Reset trigger. Whenever `reset>0`, the internal state `x` and covariance matrix `P` are reset.
* `u`: Control input (Mx1)
* `z`: Measurement signal (Mx1)
#### Example test programs
Demo 1 `(N=1, M=1)` (don't listen, just use oscilloscope):
```faust
process = fi.kalman(N, M, B, R, H, Q, F, reset, u, z) : it.interpolate_linear(filteredAmt, z)
with {
B = 1.;
R = 0.1;
H = 1;
Q = .01; 
F = la.identity(N);
reset = button("reset");

Dimensions
N = 1; // State size
M = 1; // Measurement size

freq = hslider("Freq", 1, 0.01, 10, .01);
u = 0.; // constant input
trueState = os.osc(freq)*.5 + u;
noiseGain = hslider("Noise Gain", .1, 0, 1, .01);

filteredAmt = hslider("Filter Amount", 1, 0, 1, .01) : si.smoo;

measurementNoise = no.noise*noiseGain;
z = trueState + measurementNoise; // Observed state
};
```
Demo 2 `(N=2, M=1)` (don't listen, just use oscilloscope)
```faust
process = fi.kalman(N, M, B, R, H, Q, F, reset, u, z)
with {
B = par(i, N, 0);
R = (0.1);
H = (1, 0);
Q = la.diag(2, par(i, N, .1));
F = la.identity(N);
reset = 0;
u = si.bus(M);
z = si.bus(M);

Dimensions
N = 2; // State size
M = 1; // Measurement size
};
```
#### References
* <https://en.wikipedia.org/wiki/Kalman_filter>
* <https://www.cs.unc.edu/~welch/kalman/index.html>

---

# hoa.lib
**Prefix:** `ho`

################################ hoa.lib ##########################################
Higher-Order Ambisonics (HOA) library. Its official prefix is `ho`.

The HOA library provides functions and components for spatial audio rendering
and analysis using Higher-Order Ambisonics. It includes encoders, decoders,
rotators, and utilities for spherical harmonics and spatial transformations.
The library supports both 2D and 3D HOA processing workflows for immersive audio.

The HOA library is organized into 4 sections:

* [Encoding/decoding Functions](#encodingdecoding-functions)
* [Optimization Functions](#optimization-functions)
* [Spatial Sound Processes](#spatial-sound-processes)
* [3D Functions](#3d-functions)

#### References

* <https://github.com/grame-cncm/faustlibraries/blob/master/hoa.lib>
########################################################################################

## ho.encoder

----------------------`(ho.)encoder`---------------------------------
Ambisonic encoder. Encodes a signal in the circular harmonics domain
depending on an order of decomposition and an angle.
#### Usage
```faust
encoder(N, x, a) : _
```
Where:
* `N`: the ambisonic order (constant numerical expression)
* `x`: the signal
* `a`: the angle
#### Test
```faust
ho = library("hoa.lib");
os = library("oscillators.lib");
encoder_test = ho.encoder(1, os.osc(440), 0.0);
```

---

## ho.rEncoder

-------`(ho.)rEncoder`----------
Ambisonic encoder in 2D including source rotation. A mono signal is encoded at a certain ambisonic order
with two possible modes: either rotation with an angular speed, or static with a fixed angle (when speed is zero).
#### Usage
```faust
_ : rEncoder(N, sp, a, it) : _,_, ...
```
Where:
* `N`: the ambisonic order (constant numerical expression)
* `sp`: the azimuth speed expressed as angular speed (2PI/sec), positive or negative
* `a`: the fixed azimuth when the rotation stops (sp = 0) in radians
* `it` : interpolation time (in milliseconds) between the rotation and the fixed modes
#### Test
```faust
ho = library("hoa.lib");
os = library("oscillators.lib");
rEncoder_test = os.osc(440) : ho.rEncoder(1, 0.5, 0.0, 0.05);
```

---

## ho.stereoEncoder

-------`(ho.)stereoEncoder`----------
Encoding of a stereo pair of channels with symetric angles (a/2, -a/2).
#### Usage
```faust
_,_ : stereoEncoder(N, a) : _,_, ...
```
Where:
* `N`: the ambisonic order (constant numerical expression)
* `a` : opening angle in radians, left channel at a/2 angle, right channel at -a/2 angle
#### Test
```faust
ho = library("hoa.lib");
os = library("oscillators.lib");
stereoEncoder_test = os.osc(440), os.osc(660) : ho.stereoEncoder(1, 1.0);
```

---

## ho.multiEncoder

-------`(ho.)multiEncoder`----------
Encoding of a set of P signals distributed on the unit circle according to a list of P speeds and P angles.
#### Usage
```faust
_,_, ... : multiEncoder(N, lspeed, langle, it) : _,_, ...
```
Where:
* `N`: the ambisonic order (constant numerical expression)
* `lspeed` : a list of P speeds in turns by second (one speed per input signal, positive or negative)
* `langle` : a list of P angles in radians on the unit circle to localize the sources (one angle per input signal)
* `it` : interpolation time (in milliseconds) between the rotation and the fixed modes.
#### Test
```faust
ho = library("hoa.lib");
os = library("oscillators.lib");
multiEncoder_test = os.osc(440), os.osc(660) : ho.multiEncoder(1, (0.0, 0.0), (0.0, 1.57), 0.05);
```

---

## ho.decoder

--------------------------`(ho.)decoder`--------------------------------
Decodes an ambisonics sound field for a circular array of loudspeakers.
#### Usage
```faust
_ : decoder(N, P) : _
```
Where:
* `N`: the ambisonic order (constant numerical expression)
* `P`: the number of speakers (constant numerical expression)
#### Test
```faust
ho = library("hoa.lib");
os = library("oscillators.lib");
ambi = ho.encoder(1, os.osc(440), 0.0);
decoder_test = ambi : ho.decoder(1, 4);
```
#### Note
The number of loudspeakers must be greater or equal to 2n+1.
It's preferable to use 2n+2 loudspeakers.

---

## ho.decoderStereo

-----------------------`(ho.)decoderStereo`------------------------
Decodes an ambisonic sound field for stereophonic configuration.
An "home made" ambisonic decoder for stereophonic restitution
(30° - 330°): Sound field lose energy around 180°. You should
use `inPhase` optimization with ponctual sources.
#### Usage
```faust
_ : decoderStereo(N) : _
```
Where:
* `N`: the ambisonic order (constant numerical expression)
#### Test
```faust
ho = library("hoa.lib");
os = library("oscillators.lib");
ambi = ho.encoder(1, os.osc(440), 0.0);
decoderStereo_test = ambi : ho.decoderStereo(1);
```

---

## ho.iBasicDecoder

-------`(ho.)iBasicDecoder`----------
The irregular basic decoder is a simple decoder that projects the incoming ambisonic situation
to the loudspeaker situation (P loudspeakers) whatever it is, without compensation.
When there is a strong irregularity, there can be some discontinuity in the sound field.
#### Usage
```faust
_,_, ... : iBasicDecoder(N,la, direct, shift) : _,_, ...
```
Where:
* `N`: the ambisonic order (there are 2*N+1 inputs to this function)
* `la` : the list of P angles in degrees, for instance (0, 85, 182, 263) for four loudspeakers
* `direct`: 1 for direct mode, -1 for the indirect mode (changes the rotation direction)
* `shift` : angular shift in degrees to easily adjust angles
#### Test
```faust
ho = library("hoa.lib");
os = library("oscillators.lib");
ambi = ho.encoder(1, os.osc(440), 0.0);
iBasicDecoder_test = ambi : ho.iBasicDecoder(1, (0, 120, 240), 1, 0);
```

---

## ho.circularScaledVBAP

-------`(ho.)circularScaledVBAP`----------
The function provides a circular scaled VBAP with all loudspeakers and the virtual source on the unit-circle.
#### Usage
```faust
_ : circularScaledVBAP(l, t) : _,_, ...
```
Where:
* `l` : the list of angles of the loudspeakers in degrees, for instance (0, 85, 182, 263) for four loudspeakers
* `t` : the current angle of the virtual source in degrees
#### Test
```faust
ho = library("hoa.lib");
os = library("oscillators.lib");
circularScaledVBAP_test = os.osc(440) : ho.circularScaledVBAP((0, 120, 240), 60);
```

---

## ho.imlsDecoder

-------`(ho.)imlsDecoder`----------
Irregular decoder in 2D for an irregular configuration of P loudspeakers
using 2D VBAP for compensation.
#### Usage
```faust
_,_, ... : imlsDecoder(N,la, direct, shift) : _,_, ...
```
Where:
* `N`: the ambisonic order (constant numerical expression)
* `la` : the list of P angles in degrees, for instance (0, 85, 182, 263) for four loudspeakers
* `direct`: 1 for direct mode, -1 for the indirect mode (changes the rotation direction)
* `shift` : angular shift in degrees to easily adjust angles
#### Test
```faust
ho = library("hoa.lib");
os = library("oscillators.lib");
ambi = ho.encoder(1, os.osc(440), 0.0);
imlsDecoder_test = ambi : ho.imlsDecoder(1, (0, 90, 180, 270), 1, 0);
```

---

## ho.iDecoder

-------`(ho.)iDecoder`----------
General decoder in 2D enabling an irregular multi-loudspeaker configuration
and to switch between multi-channel and stereo.
#### Usage
```faust
_,_, ... : iDecoder(N, la, direct, st, g) : _,_, ...
```
Where:
* `N`: the ambisonic order (constant numerical expression)
* `la`: the list of angles in degrees
* `direct`: 1 for direct mode, -1 for the indirect mode (changes the rotation direction)
* `shift` : angular shift in degrees to easily adjust angles
* `st`: 1 for stereo, 0 for multi-loudspeaker configuration. When 1, stereo sounds goes through the first two channels
* `g` : gain between 0 and 1
#### Test
```faust
ho = library("hoa.lib");
os = library("oscillators.lib");
ambi = ho.encoder(1, os.osc(440), 0.0);
iDecoder_test = (ambi, 0.0) : ho.iDecoder(1, (0, 120, 240), 1, 0, 0.8);
```

---

## ho.optimBasic

----------------`(ho.)optimBasic`-------------------------
The basic optimization has no effect and should be used for a perfect
circle of loudspeakers with one listener at the perfect center loudspeakers
array.
#### Usage
```faust
_ : optimBasic(N) : _
```
Where:
* `N`: the ambisonic order (constant numerical expression)
#### Test
```faust
ho = library("hoa.lib");
os = library("oscillators.lib");
ambi = ho.encoder(1, os.osc(440), 0.0);
optimBasic_test = ambi : ho.optimBasic(1);
```

---

## ho.optimMaxRe

----------------`(ho.)optimMaxRe`-------------------------
The maxRe optimization optimizes energy vector. It should be used for an
auditory confined in the center of the loudspeakers array.
#### Usage
```faust
_ : optimMaxRe(N) : _
```
Where:
* `N`: the ambisonic order (constant numerical expression)
#### Test
```faust
ho = library("hoa.lib");
os = library("oscillators.lib");
ambi = ho.encoder(1, os.osc(440), 0.0);
optimMaxRe_test = ambi : ho.optimMaxRe(1);
```

---

## ho.optimInPhase

----------------`(ho.)optimInPhase`-------------------------
The inPhase optimization optimizes energy vector and put all loudspeakers signals
in phase. It should be used for an auditory.
#### Usage
```faust
_ : optimInPhase(N) : _
```
Where:
* `N`: the ambisonic order (constant numerical expression)
#### Test
```faust
ho = library("hoa.lib");
os = library("oscillators.lib");
ambi = ho.encoder(1, os.osc(440), 0.0);
optimInPhase_test = ambi : ho.optimInPhase(1);
```

---

## ho.optim

-------`(ho.)optim`----------
Ambisonic optimizer including the three elementary optimizers:
`(ho).optimBasic`, `(ho).optimMaxRe` and `(ho.)optimInPhase`.
#### Usage
```faust
_,_, ... : optim(N, ot) : _,_, ...
```
Where:
* `N`: the ambisonic order (constant numerical expression)
* `ot` : optimization type (0 for `optimBasic`, 1 for `optimMaxRe`, 2 for `optimInPhase`)
#### Test
```faust
ho = library("hoa.lib");
os = library("oscillators.lib");
ambi = ho.encoder(1, os.osc(440), 0.0);
optim_test = ambi : ho.optim(1, 1);
```

---

## ho.wider

----------------`(ho.)wider`-------------------------
Can be used to wide the diffusion of a localized sound. The order
depending signals are weighted and appear in a logarithmic way to
have linear changes.
#### Usage
```faust
_ : wider(N,w) : _
```
Where:
* `N`: the ambisonic order (constant numerical expression)
* `w`: the width value between 0 - 1
#### Test
```faust
ho = library("hoa.lib");
os = library("oscillators.lib");
ambi = ho.encoder(1, os.osc(440), 0.0);
wider_test = ambi : ho.wider(1, 0.5);
```

---

## ho.mirror

-------`(ho.)mirror`----------
Mirroring effect on the sound field.
#### Usage
```faust
_,_, ... : mirror(N, fa) : _,_, ...
```
Where:
* `N`: the ambisonic order (constant numerical expression)
* `fa` : mirroring type (1 = original sound field, 0 = original+mirrored sound field, -1 = mirrored sound field)
#### Test
```faust
ho = library("hoa.lib");
os = library("oscillators.lib");
ambi = ho.encoder(1, os.osc(440), 0.0);
mirror_test = ambi : ho.mirror(1, -1);
```

---

## ho.map

----------------`(ho.)map`-------------------------
It simulates the distance of the source by applying a gain
on the signal and a wider processing on the soundfield.
#### Usage
```faust
map(N, x, r, a)
```
Where:
* `N`: the ambisonic order (constant numerical expression)
* `x`: the signal
* `r`: the radius
* `a`: the angle in radian
#### Test
```faust
ho = library("hoa.lib");
os = library("oscillators.lib");
map_test = ho.map(1, os.osc(440), 0.5, 0.0);
```

---

## ho.rotate

----------------`(ho.)rotate`-------------------------
Rotates the sound field.
#### Usage
```faust
_ : rotate(N, a) : _
```
Where:
* `N`: the ambisonic order (constant numerical expression)
* `a`: the angle in radian
#### Test
```faust
ho = library("hoa.lib");
os = library("oscillators.lib");
rotate_test = ho.encoder(1, os.osc(440), 0.0) : ho.rotate(1, 0.78);
```

---

## ho.scope

-------`(ho.)scope`----------
Produces an XY pair of signals representing the ambisonic sound field.
#### Usage
```faust
_,_, ... : scope(N, rt) : _,_
```
Where:
* `N`: the ambisonic order (constant numerical expression)
* `rt` : refreshment time in milliseconds
#### Test
```faust
ho = library("hoa.lib");
os = library("oscillators.lib");
scope_test = ho.encoder(1, os.osc(440), 0.0) : ho.scope(1, 0.1);
```

---

## ho.encoder3D

----------------------`(ho.)encoder3D`---------------------------------
Ambisonic encoder. Encodes a signal in the circular harmonics domain
depending on an order of decomposition, an angle and an elevation.
#### Usage
```faust
encoder3D(N, x, a, e) : _
```
Where:
* `N`: the ambisonic order (constant numerical expression)
* `x`: the signal
* `a`: the angle
* `e`: the elevation
#### Test
```faust
ho = library("hoa.lib");
os = library("oscillators.lib");
encoder3D_test = ho.encoder3D(1, os.osc(440), 0.0, 0.0);
```

---

## ho.rEncoder3D

-------`(ho.)rEncoder3D`----------
Ambisonic encoder in 3D including source rotation. A mono signal is encoded at at certain ambisonic order
with two possible modes: either rotation with 2 angular speeds (azimuth and elevation), or static with a fixed pair of angles.
`rEncoder3D` is a standard Faust function.
#### Usage
```faust
_ : rEncoder3D(N, azsp, elsp, az, el, it) : _,_, ...
```
Where:
* `N`: the ambisonic order (constant numerical expression)
* `azsp`: the azimuth speed expressed as angular speed (2PI/sec), positive or negative
* `elsp`: the elevation speed expressed as angular speed (2PI/sec), positive or negative
* `az`: the fixed azimuth when the azimuth rotation stops (azsp = 0) in radians
* `el`: the fixed elevation when the elevation rotation stops (elsp = 0) in radians
* `it` : interpolation time (in milliseconds) between the rotation and the fixed modes
#### Test
```faust
ho = library("hoa.lib");
os = library("oscillators.lib");
rEncoder3D_test = os.osc(440) : ho.rEncoder3D(1, 0.5, 0.3, 0.0, 0.0, 0.05);
```

---

## ho.optimBasic3D

----------------`(ho.)optimBasic3D`-------------------------
The basic optimization has no effect and should be used for a perfect
sphere of loudspeakers with one listener at the perfect center loudspeakers
array.
#### Usage
```faust
_ : optimBasic3D(N) : _
```
Where:
* `N`: the ambisonic order (constant numerical expression)
#### Test
```faust
ho = library("hoa.lib");
os = library("oscillators.lib");
ambi3D = ho.encoder3D(1, os.osc(440), 0.0, 0.0);
optimBasic3D_test = ambi3D : ho.optimBasic3D(1);
```

---

## ho.optimMaxRe3D

----------------`(ho.)optimMaxRe3D`-------------------------
The maxRe optimization optimize energy vector. It should be used for an
auditory confined in the center of the loudspeakers array.
#### Usage
```faust
_ : optimMaxRe3D(N) : _
```
Where:
* `N`: the ambisonic order (constant numerical expression)
#### Test
```faust
ho = library("hoa.lib");
os = library("oscillators.lib");
ambi3D = ho.encoder3D(1, os.osc(440), 0.0, 0.0);
optimMaxRe3D_test = ambi3D : ho.optimMaxRe3D(1);
```

---

## ho.optimInPhase3D

----------------`(ho.)optimInPhase3D`-------------------------
The inPhase Optimization optimizes energy vector and put all loudspeakers signals
in phase. It should be used for an auditory.
#### Usage
```faust
_ : optimInPhase3D(N) : _
```
Where:
* `N`: the ambisonic order (constant numerical expression)
#### Test
```faust
ho = library("hoa.lib");
os = library("oscillators.lib");
ambi3D = ho.encoder3D(1, os.osc(440), 0.0, 0.0);
optimInPhase3D_test = ambi3D : ho.optimInPhase3D(1);
```

---

## ho.optim3D

-------`(ho.)optim3D`----------
Ambisonic optimizer including the three elementary optimizers:
`(ho).optimBasic3D`, `(ho).optimMaxRe3D` and `(ho.)optimInPhase3D`.
#### Usage
```faust
_,_, ... : optim3D(N, ot) : _,_, ...
```
Where:
* `N`: the ambisonic order (constant numerical expression)
* `ot` : optimization type (0 for optimBasic, 1 for optimMaxRe, 2 for optimInPhase)
#### Test
```faust
ho = library("hoa.lib");
os = library("oscillators.lib");
ambi3D = ho.encoder3D(1, os.osc(440), 0.0, 0.0);
optim3D_test = ambi3D : ho.optim3D(1, 2);
```

---

# instruments.lib
**Prefix:** `in`

instruments.lib - Faust function of various types useful for building physical model instruments

# interpolators.lib
**Prefix:** `it`

#################################### interpolators.lib ########################################
A library to handle interpolation. Its official prefix is `it`.

This library provides interpolation algorithms for signal and control
processing. It includes linear, polynomial, spline, and higher-order interpolation
methods used in delay lines, envelope shaping, resampling, and parameter smoothing.

The Interpolators library is organized into 7 sections:

* [Two points interpolation functions](#two-points-interpolation-functions)
* [Four points interpolation functions](#four-points-interpolation-functions)
* [Two points interpolators](#two-points-interpolators)
* [Four points interpolators](#four-points-interpolators)
* [Generic piecewise linear interpolation](#generic-piecewise-linear-interpolation)
* [Lagrange based interpolators](#lagrange-based-interpolators)
* [Misc functions](#misc-functions)

The first four sections provide several basic interpolation functions, as well as interpolators
taking a `gen` circuit of N outputs producing values to be interpolated, triggered
by a `idv` read index signal. Two points and four points interpolations are implemented.

The `idv` parameter is to be used as a read index. In `-single` (= singleprecision) mode,
a technique based on 2 signals with the pure integer index and a fractional part in the [0,1]
range is used to avoid accumulating errors. In `-double` (= doubleprecision) or `-quad` (= quadprecision) modes,
a standard implementation with a single fractional index signal is used. Three functions `int_part`, `frac_part` and `mak_idv` are available to manipulate the read index signal.

Here is a use-case with `waveform`. Here the signal given to `interpolator_XXX` uses the `idv` model.

```
waveform_interpolator(wf, step, interp) = interp(gen, idv)
with {
gen(idx) = wf, (idx:max(0):min(size-1)) : rdtable with { size = wf:(_,!); };   /* waveform size */
index = (+(step)~_)-step;  /* starting from 0 */
idv = it.make_idv(index);  /* build the signal for interpolation in a generic way */
};

waveform_linear(wf, step) = waveform_interpolator(wf, step, it.interpolator_linear);
waveform_cosine(wf, step) = waveform_interpolator(wf, step, it.interpolator_cosine);
waveform_cubic(wf, step) = waveform_interpolator(wf, step, it.interpolator_cubic);

waveform_interp(wf, step, selector) = waveform_interpolator(wf, step, interp_select(selector))
with {
/* adapts the argument order */
interp_select(sel, gen, idv) = it.interpolator_select(gen, idv, sel);
};

waveform and index
waveform_interpolator1(wf, idv, interp) = interp(gen, idv)
with {
gen(idx) = wf, (idx:max(0):min(size-1)) : rdtable with { size = wf:(_,!); };   /* waveform size */

## it.interpolate_linear

-------`(it.)interpolate_linear`----------
Linear interpolation between 2 values.
#### Usage
```faust
interpolate_linear(dv,v0,v1) : _
```
Where:
* `dv`: in the fractional value in [0..1] range
* `v0`: is the first value
* `v1`: is the second value
#### Test
```faust
it = library("interpolators.lib");
interpolate_linear_test = it.interpolate_linear(0.5, 0.0, 1.0);
```
#### References
* <https://github.com/jamoma/JamomaCore/blob/master/Foundation/library/includes/TTInterpolate.h>

---

## it.interpolate_cosine

-------`(it.)interpolate_cosine`----------
Cosine interpolation between 2 values.
#### Usage
```faust
interpolate_cosine(dv,v0,v1) : _
```
Where:
* `dv`: in the fractional value in [0..1] range
* `v0`: is the first value
* `v1`: is the second value
#### Test
```faust
it = library("interpolators.lib");
interpolate_cosine_test = it.interpolate_cosine(0.5, 0.0, 1.0);
```
#### References
* <https://github.com/jamoma/JamomaCore/blob/master/Foundation/library/includes/TTInterpolate.h>

---

## it.interpolate_cubic

-------`(it.)interpolate_cubic`----------
Cubic interpolation between 4 values.
#### Usage
```faust
interpolate_cubic(dv,v0,v1,v2,v3) : _
```
Where:
* `dv`: in the fractional value in [0..1] range
* `v0`: is the first value
* `v1`: is the second value
* `v2`: is the third value
* `v3`: is the fourth value
#### Test
```faust
it = library("interpolators.lib");
interpolate_cubic_test = it.interpolate_cubic(0.5, -1.0, 2.0, 1.0, 4.0);
```
#### References
* <https://www.paulinternet.nl/?page=bicubic>

---

## it.interpolator_two_points

-------`(it.)interpolator_two_points`----------
Generic interpolator on two points (current and next index), assuming an increasing index.
#### Usage
```faust
interpolator_two_points(gen, idv, interpolate_two_points) : si.bus(outputs(gen))
```
Where:
* `gen`: a circuit with an 'idv' reader input that produces N outputs
* `idv`: a fractional read index expressed as a float value, or a (int,frac) pair
* `interpolate_two_points`: a two points interpolation function
#### Test
```faust
it = library("interpolators.lib");
ma = library("maths.lib");
interpolator_two_points_test = it.interpolator_two_points(gen, idv, it.interpolate_linear)
with {
gen(idx) = waveform {0.0, 1.0, 4.0, 9.0, 16.0}, int(ma.modulo(idx, 5)) : rdtable;
step = 0.25;
idxFloat = ma.modulo((+(step)~_) - step, 4.0);
idv = it.make_idv(idxFloat);
};
```

---

## it.interpolator_linear

-------`(it.)interpolator_linear`----------
Linear interpolator for a 'gen' circuit triggered by an 'idv' input to generate values.
#### Usage
```faust
interpolator_linear(gen, idv) : si.bus(outputs(gen))
```
Where:
* `gen`: a circuit with an 'idv' reader input that produces N outputs
* `idv`: a fractional read index expressed as a float value, or a (int,frac) pair
#### Test
```faust
it = library("interpolators.lib");
ma = library("maths.lib");
interpolator_linear_test = it.interpolator_linear(gen, idv)
with {
gen(idx) = waveform {0.0, 1.0, 4.0, 9.0, 16.0}, int(ma.modulo(idx, 5)) : rdtable;
step = 0.25;
idxFloat = ma.modulo((+(step)~_) - step, 4.0);
idv = it.make_idv(idxFloat);
};
```

---

## it.interpolator_cosine

-------`(it.)interpolator_cosine`----------
Cosine interpolator for a 'gen' circuit triggered by an 'idv' input to generate values.
#### Usage
```faust
interpolator_cosine(gen, idv) : si.bus(outputs(gen))
```
Where:
* `gen`: a circuit with an 'idv' reader input that produces N outputs
* `idv`: a fractional read index expressed as a float value, or a (int,frac) pair
#### Test
```faust
it = library("interpolators.lib");
ma = library("maths.lib");
interpolator_cosine_test = it.interpolator_cosine(gen, idv)
with {
gen(idx) = waveform {0.0, 1.0, 4.0, 9.0, 16.0}, int(ma.modulo(idx, 5)) : rdtable;
step = 0.25;
idxFloat = ma.modulo((+(step)~_) - step, 4.0);
idv = it.make_idv(idxFloat);
};
```

---

## it.interpolator_four_points

-------`(it.)interpolator_four_points`----------
Generic interpolator on interpolator_four_points points (previous, current and two next indexes), assuming an increasing index.
#### Usage
```faust
interpolator_four_points(gen, idv, interpolate_four_points) : si.bus(outputs(gen))
```
Where:
* `gen`: a circuit with an 'idv' reader input that produces N outputs
* `idv`: a fractional read index expressed as a float value, or a (int,frac) pair
* `interpolate_four_points`: a four points interpolation function
#### Test
```faust
it = library("interpolators.lib");
ma = library("maths.lib");
interpolator_four_points_test = it.interpolator_four_points(gen, idv, it.interpolate_cubic)
with {
gen(idx) = waveform {-1.0, 2.0, 1.0, 4.0, 7.0, 3.0}, int(ma.modulo(idx, 6)) : rdtable;
step = 0.25;
idxFloat = ma.modulo((+(step)~_) - step, 5.0);
idv = it.make_idv(idxFloat);
};
```

---

## it.interpolator_cubic

-------`(it.)interpolator_cubic`----------
Cubic interpolator for a 'gen' circuit triggered by an 'idv' input to generate values.
#### Usage
```faust
interpolator_cubic(gen, idv) : si.bus(outputs(gen))
```
Where:
* `gen`: a circuit with an 'idv' reader input that produces N outputs
* `idv`: a fractional read index expressed as a float value, or a (int,frac) pair
#### Test
```faust
it = library("interpolators.lib");
ma = library("maths.lib");
interpolator_cubic_test = it.interpolator_cubic(gen, idv)
with {
gen(idx) = waveform {-1.0, 2.0, 1.0, 4.0, 7.0, 3.0}, int(ma.modulo(idx, 6)) : rdtable;
step = 0.25;
idxFloat = ma.modulo((+(step)~_) - step, 5.0);
idv = it.make_idv(idxFloat);
};
```

---

## it.interpolator_select

-------`(it.)interpolator_select`----------
Generic configurable interpolator (with selector between in [0..3]). The value 3 is used for no interpolation.
#### Usage
```faust
interpolator_select(gen, idv, sel) : _,_... (equal to N = outputs(gen))
```
Where:
* `gen`: a circuit with an 'idv' reader input that produces N outputs
* `idv`: a fractional read index expressed as a float value, or a (int,frac) pair
* `sel`: an interpolation algorithm selector in [0..3] (0 = linear, 1 = cosine, 2 = cubic, 3 = nointerp)
#### Test
```faust
it = library("interpolators.lib");
ma = library("maths.lib");
interpolator_select_test = it.interpolator_select(gen, idv, 2)
with {
gen(idx) = waveform {-1.0, 2.0, 1.0, 4.0, 7.0, 3.0}, int(ma.modulo(idx, 6)) : rdtable;
step = 0.25;
idxFloat = ma.modulo((+(step)~_) - step, 5.0);
idv = it.make_idv(idxFloat);
};
```

---

## it.lerp

-------`(it.)lerp`------------------------------------------------------------
Linear interpolation between two points.
#### Usage
```faust
lerp(x0, x1, y0, y1, x) : si.bus(1);
```
Where:
* `x0`: x-coordinate origin
* `x1`: x-coordinate destination
* `y0`: y-coordinate origin
* `y1`: y-coordinate destination
* `x`: x-coordinate input
#### Test
```faust
it = library("interpolators.lib");
lerp_test = it.lerp(0.0, 10.0, -5.0, 5.0, 2.5);
```

---

## it.piecewise

-------`(it.)piecewise`-------------------------------------------------------
Linear piecewise interpolation between N points.
#### Usage
```faust
piecewise(xList, yList, x) : si.bus(1);
```
Where:
* `xList`: x-coordinates list
* `yList`: y-coordinates list
* `x`: x-coordinate input
#### Example test program
The code below will output the values of linear segments going through the
y coordinates as the input goes from -5 to 5:
```faust
x = hslider("x", -5, -5.0, 5.0, .001);
process = it.piecewise((-5, -3, 0, 3, 5), (2, 0, 3, -3, -2), x);
```
#### Test
```faust
it = library("interpolators.lib");
piecewise_test = it.piecewise((-5, -2, 0, 3), (1, 0, 4, -1), os.osc(0.1));
```

---

## it.lagrangeCoeffs

-------`(it.)lagrangeCoeffs`---------------------------------------------
This is a function to generate N + 1 coefficients for an Nth-order Lagrange
basis polynomial with arbitrary spacing of the points.
#### Usage
```faust
lagrangeCoeffs(N, xCoordsList, x) : si.bus(N + 1)
```
Where:
* `N`: order of the interpolation filter, known at compile-time
* `xCoordsList`: a list of N + 1 elements determining the x-axis coordinates of N + 1 values, known at compile-time
* `x`: a fractional position on the x-axis to obtain the interpolated y-value
#### Test
```faust
it = library("interpolators.lib");
lagrangeCoeffs_test = it.lagrangeCoeffs(2, (0.0, 0.5, 1.0), 0.25);
```
#### References
* <https://ccrma.stanford.edu/~jos/pasp/Lagrange_Interpolation.html>
* <https://en.wikipedia.org/wiki/Lagrange_polynomial>

---

## it.lagrangeInterpolation

-------`(it.)lagrangeInterpolation`--------------------------------------
Nth-order Lagrange interpolator to interpolate between a set of arbitrarily spaced N + 1 points.
#### Usage
```faust
x , yCoords : lagrangeInterpolation(N, xCoordsList) : _
```
Where:
* `N`: order of the interpolator, known at compile-time
* `xCoordsList`: a list of N + 1 elements determining the x-axis spacing of the points, known at compile-time
* `x`: an x-axis position to interpolate between the y-values
* `yCoords`: N + 1 elements determining the values of the interpolation points
Example: find the centre position of a four-point set using an order-3
Lagrange function fitting the equally-spaced points [2, 5, -1, 3]:
```faust
N = 3;
xCoordsList = (0, 1, 2, 3);
x = N / 2.0;
yCoords = 2, 5, -1, 3;
process = x, yCoords : it.lagrangeInterpolation(N, xCoordsList);
```
which outputs ~1.938.
Example: output the dashed curve showed on the Wikipedia page (top figure in <https://en.wikipedia.org/wiki/Lagrange_polynomial>):
```faust
N = 3;
xCoordsList = (-9, -4, -1, 7);
x = os.phasor(16, 1) - 9;
yCoords = 5, 2, -2, 9;
process = x, yCoords : it.lagrangeInterpolation(N, xCoordsList);
```
#### Test
```faust
it = library("interpolators.lib");
lagrangeInterpolation_test = (lagrange_x, lagrange_y0, lagrange_y1, lagrange_y2, lagrange_y3) : it.lagrangeInterpolation(3, (0, 1, 2, 3))
with {
lagrange_x = 1.5;
lagrange_y0 = 2.0;
lagrange_y1 = 5.0;
lagrange_y2 = -1.0;
lagrange_y3 = 3.0;
};
```
#### References
* <https://ccrma.stanford.edu/~jos/pasp/Lagrange_Interpolation.html>
* Sanfilippo and Parker 2021, "Combining zeroth and first‐order analysis with Lagrange polynomials to reduce artefacts in live concatenative granular processing." Proceedings of the DAFx conference 2021, Vienna, Austria.
* <https://dafx2020.mdw.ac.at/proceedings/papers/DAFx20in21_paper_38.pdf>

---

## it.frdtable

-------`(it.)frdtable`--------------------------------------------
Look-up circular table with Nth-order Lagrange interpolation for fractional
indexes. The index is wrapped-around and the table is cycles for an index
span of size S, which is the table size in samples.
#### Usage
```faust
frdtable(N, S, init, idx) : _
```
Where:
* `N`: Lagrange interpolation order, known at compile-time
* `S`: table size in samples, known at compile-time
* `init`: the initial table content, known at compile-time
* `idx`: fractional index wrapped-around 0 and S
#### Example test program
Test the effectiveness of the 5th-order interpolation scheme by
creating a table look-up oscillator using only 16 points of a sinewave;
compare the result with a non-interpolated version:
```faust
N = 5;
S = 16;
index = os.phasor(S, 1000);
process = rdtable(S, os.sinwaveform(S), int(index)) ,
it.frdtable(N, S, os.sinwaveform(S), index);
```
#### Test
```faust
it = library("interpolators.lib");
os = library("oscillators.lib");
frdtable_test = it.frdtable(3, 16, os.sinwaveform(16), os.phasor(16, 200));
```

---

## it.frwtable

-------`(it.)frwtable`--------------------------------------------
Look-up updatable circular table with Nth-order Lagrange interpolation for
fractional indexes. The index is wrapped-around and the table is circular
indexes ranging from 0 to S, which is the table size in samples.
#### Usage
```faust
frwtable(N, S, init, w_idx, x, r_idx) : _
```
Where:
* `N`: Lagrange interpolation order, known at compile-time
* `S`: table size in samples, known at compile-time
* `init`: the initial table content, known at compile-time
* `w_idx`: it should be an INT between 0 and S - 1
* `x`: input signal written on the w_idx positions
* `r_idx`: fractional index wrapped-around 0 and S
#### Example test program
Test the effectiveness of the 5th-order interpolation scheme by
creating a table look-up oscillator using only 16 points of a sinewave;
compare the result with a non-interpolated version:
```faust
N = 5;
S = 16;
rIdx = os.phasor(S, 300);
wIdx = ba.period(S);
process = rwtable(S, os.sinwaveform(S), wIdx, os.sinwaveform(S), int(rIdx)) ,
it.frwtable(N, S, os.sinwaveform(S), wIdx, os.sinwaveform(S), rIdx);
```
#### Test
```faust
it = library("interpolators.lib");
os = library("oscillators.lib");
ba = library("basics.lib");
frwtable_test = it.frwtable(3, 16, os.sinwaveform(16), ba.period(16), os.osc(220), os.phasor(16, 150));
```

---

## it.remap

---------------`(it.)remap`---------------------------------------------
Linearly map from an input domain to an output range.
#### Usage
```faust
_ : remap(from1, from2, to1, to2) : _
```
Where:
* `from1`: the domain's lower bound.
* `from2`: the domain's upper bound.
* `to1`: the range's lower bound.
* `to2`: the range's upper bound.
Note that having `from1` == `from2` in the mapping will cause a division by zero that has to be taken in account.
#### Example test program
An oscillator remapped from [-1., 1.] to [100., 1000.]:
```faust
os.osc(440) : it.remap(-1., 1., 100., 1000.)
```
#### Test
```faust
it = library("interpolators.lib");
os = library("oscillators.lib");
remap_test = it.remap(-1.0, 1.0, 100.0, 1000.0, os.osc(0.5));
```

---

# linearalgebra.lib
**Prefix:** `la`

######################## linearalgebra.lib ######################################
Linear Algebra library. Its official prefix is `la`.

This library provides mathematical tools for matrix and vector operations
in Faust. It includes basic arithmetic, dot products, outer products, matrix inversion,
determinant computation, and utilities for linear transformations and numerical analysis.

This library adds some new linear algebra functions:

`determinant`

`minor`

`inverse`

`transpose2`

`matMul` matrix multiplication

`identity`

`diag`

How does it work? An `NxM` matrix can be flattened into a bus `si.bus(N*M)`. These buses can be passed to functions as long as `N` and sometimes `M` (if the matrix need not be square) are passed too.

#### Some things to think about going forward

##### Implications for ML in Faust

Next step of making a "Dense"/"Linear" layer from machine learning.
Where in the libraries should `ReLU` go?
What about 3D tensors instead of 2D matrices? Image convolutions take place on 3D tensors shaped `HxWxC`.

#####Design of matMul

Currently the design is `matMul(J, K, L, M, leftHandMat, rightHandMat)` where `leftHandMat` is `JxK` and `rightHandMat` is `LxM`.

It would also be neat to have `matMul(J, K, rightHandMat, L, M, leftHandMat)`.

Then a "packed" matrix could be consistently stored as a combination of a 2-channel "header" `N, M` and the values `si.bus(N*M)`.

This would ultimately enable `result = packedLeftHand : matMul(packedRightHand);` for the equivalent numpy code: `result = packedLeftHand @ packedRightHand;`.

#### References

* <https://github.com/grame-cncm/faustlibraries/blob/master/linearalgebra.lib>
#################################################################################

## la.determinant

-----------`(la.)determinant`-------------------------
Calculates the determinant of a bus that represents
an `NxN` matrix.
#### Usage
```faust
si.bus(N*N) : determinant(N) : _
```
Where:
* `N`: the size of each axis of the matrix.
#### Test
```faust
la = library("linearalgebra.lib");
determinant_test = (1, 2, 3, 4) : la.determinant(2);
```

---

## la.minor

-----------`(la.)minor`----------------------------------------------------
An utility for finding the matrix minor when inverting a matrix.
It returns the determinant of the submatrix formed by deleting the row at
index `ROW` and column at index `COL`.
The following implementation doesn't work but looks simple.
```faust
minor(N, ROW, COL) = par(r, N, par(c, N, select2((ROW==r)||(COL==c),_,!))) : determinant(N-1);
```
#### Usage
```faust
si.bus(N*N) : minor(N, ROW, COL) : _
```
Where:
* `N`: the size of each axis of the matrix.
* `ROW`: the selected position on 0th dimension of the matrix (`0 <= ROW < N`)
* `COL`: the selected position on the 1st dimension of the matrix (`0 <= COL < N`)
#### Test
```faust
la = library("linearalgebra.lib");
minor_test = (1, 2, 3, 0, 4, 5, 7, 8, 9) : la.minor(3, 1, 1);
```
#### References
* <https://en.wikipedia.org/wiki/Minor_(linear_algebra)#First_minor>

---

## la.inverse

-----------`(la.)inverse`---------------------------------------------
Inverts a matrix. The incoming bus represents an `NxN` matrix.
Note, this is an unsafe operation since not all matrices are invertible.
#### Usage
```faust
si.bus(N*N) : inverse(N) : si.bus(N*N)
```
Where:
* `N`: the size of each axis of the matrix.
#### Test
```faust
la = library("linearalgebra.lib");
inverse_test = (4, 7, 2, 6) : la.inverse(2);
```

---

## la.transpose2

--------------`(la.)transpose2`-----------------------------------
Transposes an `NxM` matrix stored in row-major order, resulting
in an `MxN` matrix stored in row-major order.
#### Usage
```faust
si.bus(N*M) : transpose2(N, M) : si.bus(M*N)
```
Where:
* `N`: the number of rows in the input matrix
* `M`: the number of columns in the input matrix
#### Test
```faust
la = library("linearalgebra.lib");
transpose2_test = (1, 2, 3, 4, 5, 6) : la.transpose2(2, 3);
```

---

## la.matMul

--------------`(la.)matMul`---------------------------------------------
Multiply a `JxK` matrix (mat1) and an `LxM` matrix (mat2) to produce a `JxM` matrix.
Note that `K==L`.
Both matrices should use row-major order.
In terms of numpy, this function is `mat1 @ mat2`.
#### Usage
```faust
matMul(J, K, L, M, si.bus(J*K), si.bus(L*M)) : si.bus(J*M)
```
Where:
* `J`: the number of rows in `mat1`
* `K`: the number of columns in `mat1`
* `L`: the number of rows in `mat2`
* `M`: the number of columns in `mat2`
#### Test
```faust
la = library("linearalgebra.lib");
matMul_test = (1, 2, 3, 4), (5, 6, 7, 8) : la.matMul(2, 2, 2, 2);
```

---

## la.identity

---------------`(la.)identity`-------------------------
Creates an `NxN` identity matrix.
#### Usage
```faust
identity(N) : si.bus(N*N)
```
Where:
* `N`: The size of each axis of the identity matrix.
#### Test
```faust
la = library("linearalgebra.lib");
identity_test = la.identity(3);
```

---

## la.diag

---------------`(la.)diag`-------------------------------
Creates a diagonal matrix of size `NxN` with specified
values along the diagonal.
#### Usage
```faust
si.bus(N) : diag(N) : si.bus(N*N)
```
Where:
* `N`: The size of each axis of the matrix.
#### Test
```faust
la = library("linearalgebra.lib");
diag_test = (1, 2, 3) : la.diag(3);
```

---

# maths.lib
**Prefix:** `ma`

################################ maths.lib ##########################################
Maths library. Its official prefix is `ma`.

This library provides mathematical functions and utilities for numerical
computations in Faust. It includes trigonometric, exponential, logarithmic, and
statistical functions, constants, and complex-number
operations used throughout Faust DSP and control code.

The Maths library is organized into 1 section:

* [Functions Reference](#functions-reference)

Some functions are implemented as Faust foreign functions of `math.h` functions
that are not part of Faust's primitives. Defines also various constants and several
utilities.

#### References

* <https://github.com/grame-cncm/faustlibraries/blob/master/maths.lib>
########################################################################################
## History
* 06/13/2016 [RM]  normalizing and integrating to new libraries
* 07/08/2015 [YO]  documentation comments
* 20/06/2014 [SL]  added FTZ function
* 22/06/2013 [YO]  added float|double|quad variants of some foreign functions
* 28/06/2005 [YO]  postfixed functions with 'f' to force float version instead of double
* 28/06/2005 [YO]  removed 'modf' because it requires a pointer as argument

## ma.SR

---------------------------------`(ma.)SR`---------------------------------------
Current sampling rate given at init time. Constant during program execution.
#### Usage
```faust
SR : _
```
Where:
* `SR`: initialization-time sampling rate constant
#### Test
```faust
ma = library("maths.lib");
SR_test = ma.SR;
```

---

## ma.T

---------------------------------`(ma.)T`---------------------------------------
Current sample duration in seconds computed from the sampling rate given at init time. Constant during program execution.
#### Usage
```faust
T : _
```
Where:
* `T`: sample duration (`1/SR`) constant
#### Test
```faust
ma = library("maths.lib");
T_test = ma.T;
```

---

## ma.BS

---------------------------------`(ma.)BS`---------------------------------------
Current block-size. Can change during the execution at each block.
#### Usage
```faust
BS : _
```
Where:
* `BS`: current processing block size
#### Test
```faust
ma = library("maths.lib");
BS_test = ma.BS;
```

---

## ma.PI

---------------------------------`(ma.)PI`---------------------------------------
Constant PI in double precision.
#### Usage
```faust
PI : _
```
Where:
* `PI`: double-precision π constant
#### Test
```faust
ma = library("maths.lib");
PI_test = ma.PI;
```

---

## ma.deg2rad

---------------------------------`(ma.)deg2rad`----------------------------------
Convert degrees to radians.
#### Usage
```faust
45. : deg2rad
```
Where:
* input: angle in degrees to convert
#### Test
```faust
ma = library("maths.lib");
deg2rad_test = 45.0 : ma.deg2rad;
```

---

## ma.rad2deg

---------------------------------`(ma.)rad2deg`----------------------------------
Convert radians to degrees.
#### Usage
```faust
ma.PI : rad2deg
```
Where:
* input: angle in radians to convert
#### Test
```faust
ma = library("maths.lib");
rad2deg_test = ma.PI : ma.rad2deg;
```

---

## ma.E

---------------------------------`(ma.)E`---------------------------------------
Constant e in double precision.
#### Usage
```faust
E : _
```
Where:
* `E`: double-precision Euler's number constant
#### Test
```faust
ma = library("maths.lib");
E_test = ma.E;
```

---

## ma.EPSILON

---------------------------------`(ma.)EPSILON`---------------------------------------
Constant EPSILON available in simple/double/quad precision,
as defined in the [floating-point standard](https://en.wikipedia.org/wiki/IEEE_754)
and [machine epsilon](https://en.wikipedia.org/wiki/Machine_epsilon),
that is smallest positive number such that `1.0 + EPSILON != 1.0`.
#### Usage
```faust
EPSILON : _
```
Where:
* `EPSILON`: machine epsilon constant for the current floating-point precision
#### Test
```faust
ma = library("maths.lib");
EPSILON_test = ma.EPSILON;
```

---

## ma.MIN

---------------------------------`(ma.)MIN`---------------------------------------
Constant MIN available in simple/double/quad precision (minimal positive value).
#### Usage
```faust
MIN : _
```
Where:
* `MIN`: minimal positive normalized value for the current precision
#### Test
```faust
ma = library("maths.lib");
MIN_test = ma.MIN;
```

---

## ma.MAX

---------------------------------`(ma.)MAX`------------------------------
Constant MAX available in simple/double/quad precision (maximal positive value).
#### Usage
```faust
MAX : _
```
Where:
* `MAX`: maximal finite value for the current precision
#### Test
```faust
ma = library("maths.lib");
MAX_test = ma.MAX;
```

---

## ma.FTZ

---------------------------------`(ma.)FTZ`---------------------------------------
Flush to zero: force samples under the "maximum subnormal number"
to be zero. Usually not needed in C++ because the architecture
file take care of this, but can be useful in JavaScript for instance.
#### Usage
```faust
_ : FTZ : _
```
Where:
* `x`: input signal to flush if its magnitude is subnormal
#### Test
```faust
ma = library("maths.lib");
FTZ_test = (ma.MIN * 0.5) : ma.FTZ;
```
#### References
* <http://docs.oracle.com/cd/E19957-01/806-3568/ncg_math.html>

---

## ma.copysign

---------------------------------`(ma.)copysign`---------------------------------------
Changes the sign of x (first input) to that of y (second input).
#### Usage
```faust
_,_ : copysign : _
```
Where:
* `x`: value whose magnitude is preserved
* `y`: value providing the sign
#### Test
```faust
ma = library("maths.lib");
copysign_test = (-1.0, 2.0) : ma.copysign;
```

---

## ma.neg

---------------------------------`(ma.)neg`---------------------------------------
Invert the sign (-x) of a signal.
#### Usage
```faust
_ : neg : _
```
Where:
* `x`: value to negate
#### Test
```faust
ma = library("maths.lib");
neg_test = 3.5 : ma.neg;
```

---

## ma.not

---------------------------------`(ma.)not`---------------------------------------
Bitwise `not` implemented with [xor](https://faustdoc.grame.fr/manual/syntax/#xor-primitive) as `not(x) = x xor -1;`.
So working regardless of the size of the integer, assuming negative numbers in two's complement.
#### Usage
```faust
_ : not : _
```
Where:
* `x`: integer input value
#### Test
```faust
ma = library("maths.lib");
not_test = 5 : ma.not;
```

---

## ma.inv

---------------------------------`(ma.)inv`---------------------------------------
Compute the inverse (1/x) of the input signal.
#### Usage
```faust
_ : inv : _
```
Where:
* `x`: denominator input (non-zero)
#### Test
```faust
ma = library("maths.lib");
inv_test = 4.0 : ma.inv;
```

---

## ma.cbrt

---------------------------------`(ma.)cbrt`--------------------------------------
Computes the cube root of of the input signal.
#### Usage
```faust
_ : cbrt : _
```
Where:
* `x`: value whose cube root is computed
#### Test
```faust
ma = library("maths.lib");
cbrt_test = 8.0 : ma.cbrt;
```

---

## ma.hypot

---------------------------------`(ma.)hypot`-------------------------------------
Computes the euclidian distance of the two input signals
sqrt(x*x+y*y) without undue overflow or underflow.
#### Usage
```faust
_,_ : hypot : _
```
Where:
* `x`: first operand
* `y`: second operand
#### Test
```faust
ma = library("maths.lib");
hypot_test = (3.0, 4.0) : ma.hypot;
```

---

## ma.ldexp

---------------------------------`(ma.)ldexp`-------------------------------------
Takes two input signals: x and n, and multiplies x by 2 to the power n.
#### Usage
```faust
_,_ : ldexp : _
```
Where:
* `x`: significand input
* `n`: exponent (integer) input
#### Test
```faust
ma = library("maths.lib");
ldexp_test = (1.5, 3) : ma.ldexp;
```

---

## ma.scalb

---------------------------------`(ma.)scalb`-------------------------------------
Takes two input signals: x and n, and multiplies x by 2 to the power n.
#### Usage
```faust
_,_ : scalb : _
```
Where:
* `x`: significand input
* `n`: exponent (integer) input
#### Test
```faust
ma = library("maths.lib");
scalb_test = (2.0, -1) : ma.scalb;
```

---

## ma.log1p

---------------------------------`(ma.)log1p`----------------------------------
Computes log(1 + x) without undue loss of accuracy when x is nearly zero.
#### Usage
```faust
_ : log1p : _
```
Where:
* `x`: offset used in `log(1 + x)` (must be greater than -1)
#### Test
```faust
ma = library("maths.lib");
log1p_test = 0.5 : ma.log1p;
```

---

## ma.logb

---------------------------------`(ma.)logb`---------------------------------------
Return exponent of the input signal as a floating-point number.
#### Usage
```faust
_ : logb : _
```
Where:
* `x`: positive value whose exponent part is returned
#### Test
```faust
ma = library("maths.lib");
logb_test = 8.0 : ma.logb;
```

---

## ma.ilogb

---------------------------------`(ma.)ilogb`-------------------------------------
Return exponent of the input signal as an integer number.
#### Usage
```faust
_ : ilogb : _
```
Where:
* `x`: positive value whose exponent part is returned
#### Test
```faust
ma = library("maths.lib");
ilogb_test = 8.0 : ma.ilogb;
```

---

## ma.log2

---------------------------------`(ma.)log2`-------------------------------------
Returns the base 2 logarithm of x.
#### Usage
```faust
_ : log2 : _
```
Where:
* `x`: positive value whose base-2 logarithm is computed
#### Test
```faust
ma = library("maths.lib");
log2_test = 8.0 : ma.log2;
```

---

## ma.expm1

---------------------------------`(ma.)expm1`-------------------------------------
Return exponent of the input signal minus 1 with better precision.
#### Usage
```faust
_ : expm1 : _
```
Where:
* `x`: input value used for the `exp(x) - 1` computation
#### Test
```faust
ma = library("maths.lib");
expm1_test = 0.5 : ma.expm1;
```

---

## ma.acosh

---------------------------------`(ma.)acosh`-------------------------------------
Computes the principle value of the inverse hyperbolic cosine
of the input signal.
#### Usage
```faust
_ : acosh : _
```
Where:
* `x`: input value (greater than or equal to 1)
#### Test
```faust
ma = library("maths.lib");
acosh_test = 1.5 : ma.acosh;
```

---

## ma.asinh

--------------------------------`(ma.)asinh`-----------------------------------
Computes the inverse hyperbolic sine of the input signal.
#### Usage
```faust
_ : asinh : _
```
Where:
* `x`: input value
#### Test
```faust
ma = library("maths.lib");
asinh_test = 0.5 : ma.asinh;
```

---

## ma.atanh

--------------------------------`(ma.)atanh`-----------------------------------
Computes the inverse hyperbolic tangent of the input signal.
#### Usage
```faust
_ : atanh : _
```
Where:
* `x`: input value in (-1, 1)
#### Test
```faust
ma = library("maths.lib");
atanh_test = 0.5 : ma.atanh;
```

---

## ma.sinh

---------------------------------`(ma.)sinh`---------------------------------------
Computes the hyperbolic sine of the input signal.
#### Usage
```faust
_ : sinh : _
```
Where:
* `x`: input value
#### Test
```faust
ma = library("maths.lib");
sinh_test = 0.5 : ma.sinh;
```

---

## ma.cosh

---------------------------------`(ma.)cosh`--------------------------------------
Computes the hyperbolic cosine of the input signal.
#### Usage
```faust
_ : cosh : _
```
Where:
* `x`: input value
#### Test
```faust
ma = library("maths.lib");
cosh_test = 0.5 : ma.cosh;
```

---

## ma.tanh

---------------------------------`(ma.)tanh`--------------------------------------
Computes the hyperbolic tangent of the input signal.
#### Usage
```faust
_ : tanh : _
```
Where:
* `x`: input value
#### Test
```faust
ma = library("maths.lib");
tanh_test = 0.5 : ma.tanh;
```

---

## ma.erf

---------------------------------`(ma.)erf`---------------------------------------
Computes the error function of the input signal.
#### Usage
```faust
_ : erf : _
```
Where:
* `x`: input value
#### Test
```faust
ma = library("maths.lib");
erf_test = 0.5 : ma.erf;
```

---

## ma.erfc

---------------------------------`(ma.)erfc`---------------------------------------
Computes the complementary error function of the input signal.
#### Usage
```faust
_ : erfc : _
```
Where:
* `x`: input value
#### Test
```faust
ma = library("maths.lib");
erfc_test = 0.5 : ma.erfc;
```

---

## ma.gamma

---------------------------------`(ma.)gamma`-------------------------------------
Computes the gamma function of the input signal.
#### Usage
```faust
_ : gamma : _
```
Where:
* `x`: positive input value
#### Test
```faust
ma = library("maths.lib");
gamma_test = 3.0 : ma.gamma;
```

---

## ma.lgamma

---------------------------------`(ma.)lgamma`------------------------------------
Calculates the natural logorithm of the absolute value of
the gamma function of the input signal.
#### Usage
```faust
_ : lgamma : _
```
Where:
* `x`: positive input value
#### Test
```faust
ma = library("maths.lib");
lgamma_test = 3.0 : ma.lgamma;
```

---

## ma.J0

----------------------------------`(ma.)J0`---------------------------------------
Computes the Bessel function of the first kind of order 0
of the input signal.
#### Usage
```faust
_ : J0 : _
```
Where:
* `x`: input value
#### Test
```faust
ma = library("maths.lib");
J0_test = 1.0 : ma.J0;
```

---

## ma.J1

----------------------------------`(ma.)J1`---------------------------------------
Computes the Bessel function of the first kind of order 1
of the input signal.
#### Usage
```faust
_ : J1 : _
```
Where:
* `x`: input value
#### Test
```faust
ma = library("maths.lib");
J1_test = 1.0 : ma.J1;
```

---

## ma.Jn

----------------------------------`(ma.)Jn`---------------------------------------
Computes the Bessel function of the first kind of order n
(first input signal) of the second input signal.
#### Usage
```faust
_,_ : Jn : _
```
Where:
* `n`: integer order
* `x`: input value
#### Test
```faust
ma = library("maths.lib");
Jn_test = (2, 1.0) : ma.Jn;
```

---

## ma.Y0

----------------------------------`(ma.)Y0`---------------------------------------
Computes the linearly independent Bessel function of the second kind
of order 0 of the input signal.
#### Usage
```faust
_ : Y0 : _
```
Where:
* `x`: positive input value
#### Test
```faust
ma = library("maths.lib");
Y0_test = 1.0 : ma.Y0;
```

---

## ma.Y1

----------------------------------`(ma.)Y1`---------------------------------------
Computes the linearly independent Bessel function of the second kind
of order 1 of the input signal.
#### Usage
```faust
_ : Y0 : _
```
Where:
* `x`: positive input value
#### Test
```faust
ma = library("maths.lib");
Y1_test = 1.0 : ma.Y1;
```

---

## ma.Yn

----------------------------------`(ma.)Yn`---------------------------------------
Computes the linearly independent Bessel function of the second kind
of order n (first input signal) of the second input signal.
#### Usage
```faust
_,_ : Yn : _
```
Where:
* `n`: integer order
* `x`: positive input value
#### Test
```faust
ma = library("maths.lib");
Yn_test = (2, 1.0) : ma.Yn;
```

---

## ma.np2

-------------------------------`(ma.)np2`--------------------------------------
Gives the next power of 2 of x.
#### Usage
```faust
np2(n) : _
```
Where:
* `n`: an integer
#### Test
```faust
ma = library("maths.lib");
np2_test = 5 : ma.np2;
```

---

## ma.frac

-----------------------------`(ma.)frac`---------------------------------------
Gives the fractional part of n.
#### Usage
```faust
frac(n) : _
```
Where:
* `n`: a decimal number
#### Test
```faust
ma = library("maths.lib");
frac_test = 3.75 : ma.frac;
```

---

## ma.modulo

-------------------------------`(ma.)modulo`---------------------------------------
Modulus operation using the `(x%y+y)%y` formula to ensures the result is always non-negative, even if `x` is negative.
#### Usage
```faust
modulo(x,y) : _
```
Where:
* `x`: the numerator
* `y`: the denominator
#### Test
```faust
ma = library("maths.lib");
modulo_test = (-3, 4) : ma.modulo;
```

---

## ma.isnan

---------------`(ma.)isnan`----------------
Return non-zero if x is a NaN.
#### Usage
```faust
isnan(x)
_ : isnan : _
```
Where:
* `x`: signal to analyse
#### Test
```faust
ma = library("maths.lib");
isnan_test = 1.0 : ma.isnan;
```

---

## ma.isinf

---------------`(ma.)isinf`----------------
Return non-zero if x is a positive or negative infinity.
#### Usage
```faust
isinf(x)
_ : isinf : _
```
Where:
* `x`: signal to analyse
#### Test
```faust
ma = library("maths.lib");
isinf_test = 1.0 : ma.isinf;
```

---

## ma.chebychev

---------------------------`(ma.)chebychev`-------------------------------
Chebychev transformation of order N.
#### Usage
```faust
_ : chebychev(N) : _
```
Where:
* `N`: the order of the polynomial, a constant numerical expression
#### Semantics
```faust
T[0](x) = 1,
T[1](x) = x,
T[n](x) = 2x*T[n-1](x) - T[n-2](x)
```
#### Test
```faust
ma = library("maths.lib");
chebychev_test = 0.5 : ma.chebychev(3);
```
#### References
* <http://en.wikipedia.org/wiki/Chebyshev_polynomial>

---

## ma.chebychevpoly

------------------------`(ma.)chebychevpoly`-------------------------------
Linear combination of the first Chebyshev polynomials.
#### Usage
```faust
_ : chebychevpoly((c0,c1,...,cn)) : _
```
Where:
* `cn`: the different Chebychevs polynomials such that:
chebychevpoly((c0,c1,...,cn)) = Sum of chebychev(i)*ci
#### Test
```faust
ma = library("maths.lib");
chebychevpoly_test = 0.5 : ma.chebychevpoly((1, 0, 1));
```
#### References
* <http://www.csounds.com/manual/html/chebyshevpoly.html>

---

## ma.diffn

------------------`(ma.)diffn`----------------------------
Negated first-order difference.
#### Usage
```faust
_ : diffn : _
```
Where:
* `x`: input signal
#### Test
```faust
ma = library("maths.lib");
os = library("oscillators.lib");
diffn_test = os.osc(440) : ma.diffn;
```

---

## ma.signum

------------------`(ma.)signum`----------------------------
The signum function signum(x) is defined as
-1 for x<0, 0 for x==0, and 1 for x>0.
#### Usage
```faust
_ : signum : _
```
Where:
* `x`: input value
#### Test
```faust
ma = library("maths.lib");
signum_test = (-5.0) : ma.signum;
```

---

## ma.nextpow2

------------------`(ma.)nextpow2`----------------------------
The nextpow2(x) returns the lowest integer m such that
2^m >= x.
#### Usage
```faust
2^nextpow2(n) : _
```
Useful for allocating delay lines, e.g.,
```faust
delay(2^nextpow2(maxDelayNeeded), currentDelay);
```
Where:
* `n`: positive value whose next power-of-two exponent is computed
#### Test
```faust
ma = library("maths.lib");
nextpow2_test = 10.0 : ma.nextpow2;
```

---

## ma.zc

--------------------`(ma.)zc`------------------------------------------------
Indicator function for zero-crossing: it returns 1 if a zero-crossing
occurs, 0 otherwise.
#### Usage
```faust
_ : zc : _
```
Where:
* `x`: input signal to monitor for zero crossings
#### Test
```faust
ma = library("maths.lib");
os = library("oscillators.lib");
zc_test = os.osc(440) : ma.zc;
```

---

## ma.primes

--------------------`(ma.)primes`------------------------------------------------
Return the n-th prime using a waveform primitive. Note that primes(0) is 2,
primes(1) is 3, and so on. The waveform is length 2048, so the largest
precomputed prime is primes(2047) which is 17863.
#### Usage
```faust
_ : primes : _
```
Where:
* `x`: index of the prime number sequence (0-based).
#### Test
```faust
ma = library("maths.lib");
primes_test = 10 : ma.primes;
```

---

# maxmsp.lib
**Prefix:** `ma`

#################################### maxmsp.lib ########################################
MaxMSP compatibility Library.

#### References
* <https://github.com/grame-cncm/faustlibraries/blob/master/maxmsp.lib>
########################################################################################

# mi.lib
**Prefix:** `mi`

############################# mi.lib #########################################
This ongoing work is the fruit of a collaboration between GRAME-CNCM and
the ANIS (Arts Numériques et Immersions Sensorielles) research group from
GIPSA-Lab (Université Grenoble Alpes).

This library implements basic 1-DoF mass-interaction physics algorithms,
allowing to declare and connect physical elements (masses, springs, non
linear interactions, etc.) together to form topological networks.
Models can be assembled by hand, however in more complex scenarios it is
recommended to use a scripting tool (such as MIMS) to generate the FAUST
signal routing for a given physical network. Its official prefix is `mi`.

[Video introduction to Mass Interaction](https://faust.grame.fr/community/events/#an-introduction-to-mass-interaction-modelling-in-faust-james-leonard-and-jerome-villeneuve)

[LAC 2019 Paper](https://hal.science/hal-02270654)

## Sources

The core mass-interaction algorithms implemented in this library are in the public
domain and are disclosed in the following scientific publications:

* Claude Cadoz, Annie Luciani, Jean-Loup Florens, Curtis Roads and Françoise
Chabade. Responsive Input Devices and Sound Synthesis by Stimulation of
Instrumental Mechanisms: The Cordis System. Computer Music Journal, Vol 8.
No. 3, 1984.
* Claude Cadoz, Annie Luciani and Jean Loup Florens. CORDIS-ANIMA: A Modeling
and Simulation System for Sound and Image Synthesis: The General Formalism.
Computer Music Journal. Vol. 17, No. 1, 1993.
* Alexandros Kontogeorgakopoulos and Claude Cadoz. Cordis Anima Physical
Modeling and Simulation System Analysis. In Proceedings of the Sound and Music
Computing Conference (SMC-07), Lefkada, Greece, 2007.
* Nicolas Castagne, Claude Cadoz, Ali Allaoui and Olivier Tache. G3: Genesis
Software Environment Update. In Proceedings of the International Computer
Music Conference (ICMC-09), Montreal, Canada, 2009.
* Nicolas Castagné and Claude Cadoz. Genesis 3: Plate-forme pour la création
musicale à l'aide des modèles physiques Cordis-Anima. In Proceedings of the
Journée de l'Informatique Musicale, Grenoble, France, 2009.
* Edgar Berdahl and Julius O. Smith. An Introduction to the Synth-A-Modeler
Compiler: Modular and Open-Source Sound Synthesis using Physical Models. In
Proceedings of the Linux Audio Conference (LAC-12), Stanford, USA, 2012.
* James Leonard and Claude Cadoz. Physical Modelling Concepts for a Collection
of Multisensory Virtual Musical Instruments. In Proceedings of the New
Interfaces for Musical Expression (NIME-15) Conference, Baton Rouge, USA, 2015.

The MI library is organized into 3 sections:

* [Utility Functions](#utility-functions)
* [Mass Algorithms](#mass-algorithms)
* [Interaction Algorithms](#interaction-algorithms)


## mi.initState

------------------------`(mi.)initState`----------------------
Used to set initial delayed position values that must be initialised
at step 0 of the physics simulation.
If you develop any of your own modules, you will need to use this (see
`mass` and `springDamper` algorithm codes for examples).
#### Usage
```faust
x : initState(x0) : _
```
Where:
* `x`: position value signal
* `x0`: initial value for position
#### Test
```faust
mi = library("mi.lib");
initState_test = button("impulse") : mi.initState(1.0);
```

---

## mi.mass

------------------------`(mi.)mass`----------------------
Implementation of a punctual mass element.
Takes an input force and produces output position.
#### Usage
```faust
mass(m, grav, x0, xr0),_ : _
```
Where:
* `m`: mass value
* `grav`: gravity force value
* `x0`: initial position
* `xr0`: initial delayed position (inferred from initial velocity)
#### Test
```faust
mi = library("mi.lib");
mass_test = 0 : mi.mass(1.0, 0.0, 0.0, 0.0);
```

---

## mi.oscil

------------------------`(mi.)oscil`----------------------
Implementation of a simple linear harmonic oscillator.
Takes an input force and produces output position.
#### Usage
```faust
oscil(m, k, z, grav, x0, xr0),_ : _
```
Where:
* `m`: mass value
* `k`: stiffness value
* `z`: damping value
* `grav`: gravity force value
* `x0`: initial position
* `xr0`: initial delayed position (inferred from initial velocity)
#### Test
```faust
mi = library("mi.lib");
oscil_test = 0 : mi.oscil(1.0, 0.5, 0.1, 0.0, 0.0, 0.0);
```

---

## mi.ground

------------------------`(mi.)ground`----------------------
Implementation of a fixed point element.
The position output produced by this module never changes, however
it still expects a force input signal (for compliance with connection
rules).
#### Usage
```faust
ground(x0),_ : _
```
Where:
* `x0`: initial position
#### Test
```faust
mi = library("mi.lib");
ground_test = 0 : mi.ground(0.0);
```

---

## mi.posInput

------------------------`(mi.)posInput`----------------------
Implementation of a position input module (driven by an outside
signal). Takes two signal inputs: incoming force (which doesn't
affect position) and the driving position signal.
#### Usage
```faust
posInput(x0),_,_ : _
```
Where:
* `x0`: initial position
#### Test
```faust
mi = library("mi.lib");
os = library("oscillators.lib");
posInput_test = 0, os.osc(1) : mi.posInput(0.0);
```

---

## mi.spring

------------------------`(mi.)spring`----------------------
Implementation of a linear elastic spring interaction.
#### Usage
```faust
spring(k, x1r, x2r),_,_ : _,_
```
Where:
* `k`: stiffness value
* `x1r`: initial delayed position of mass 1 (unused here)
* `x2r`: initial delayed position of mass 2 (unused here)
#### Test
```faust
mi = library("mi.lib");
spring_test = mi.spring(10.0, 0.0, 0.0, 0.1, -0.1);
```

---

## mi.damper

------------------------`(mi.)damper`----------------------
Implementation of a linear damper interaction.
Beware: in 32bit precision mode, damping forces can become
truncated if position values are not centered around zero!
#### Usage
```faust
damper(z, x1r, x2r),_,_ : _,_
```
Where:
* `z`: damping value
* `x1r`: initial delayed position of mass 1
* `x2r`: initial delayed position of mass 2
#### Test
```faust
mi = library("mi.lib");
damper_test = mi.damper(0.5, 0.0, 0.0, 0.2, -0.2);
```

---

## mi.springDamper

------------------------`(mi.)springDamper`----------------------
Implementation of a linear viscoelastic spring-damper interaction
(a combination of the spring and damper modules).
#### Usage
```faust
springDamper(k, z, x1r, x2r),_,_ : _,_
```
Where:
* `k`: stiffness value
* `z`: damping value
* `x1r`: initial delayed position of mass 1
* `x2r`: initial delayed position of mass 2
#### Test
```faust
mi = library("mi.lib");
springDamper_test = mi.springDamper(5.0, 0.3, 0.0, 0.0, 0.1, -0.1);
```

---

## mi.nlSpringDamper2

------------------------`(mi.)nlSpringDamper2`----------------------
Implementation of a non-linear viscoelastic spring-damper interaction
containing a quadratic term (function of squared distance).
Beware: at high displacements, this interaction will break numerical
stability conditions ! The `nlSpringDamperClipped` is a safer option.
#### Usage
```faust
nlSpringDamper2(k, q, z, x1r, x2r),_,_ : _,_
```
Where:
* `k`: linear stiffness value
* `q`: quadratic stiffness value
* `z`: damping value
* `x1r`: initial delayed position of mass 1
* `x2r`: initial delayed position of mass 2
#### Test
```faust
mi = library("mi.lib");
nlSpringDamper2_test = mi.nlSpringDamper2(5.0, 1.0, 0.2, 0.0, 0.0, 0.1, -0.1);
```

---

## mi.nlSpringDamper3

------------------------`(mi.)nlSpringDamper3`----------------------
Implementation of a non-linear viscoelastic spring-damper interaction
containing a cubic term (function of distance^3).
Beware: at high displacements, this interaction will break numerical
stability conditions ! The `nlSpringDamperClipped` is a safer option.
#### Usage
```faust
nlSpringDamper3(k, q, z, x1r, x2r),_,_ : _,_
```
Where:
* `k`: linear stiffness value
* `q`: cubic stiffness value
* `z`: damping value
* `x1r`: initial delayed position of mass 1
* `x2r`: initial delayed position of mass 2
#### Test
```faust
mi = library("mi.lib");
nlSpringDamper3_test = mi.nlSpringDamper3(5.0, 0.5, 0.2, 0.0, 0.0, 0.1, -0.1);
```

---

## mi.nlSpringDamperClipped

------------------------`(mi.)nlSpringDamperClipped`----------------------
Implementation of a non-linear viscoelastic spring-damper interaction
containing a cubic term (function of distance^3), bound by an
upper linear stiffness (hard-clipping).
This bounding means that when faced with strong displacements, the
interaction profile will "clip" at a given point and never produce
forces higher than the bounding equivalent linear spring, stopping models
from becoming unstable.
So far the interaction clips "hard" (with no soft-knee spline
interpolation, etc.)
#### Usage
```faust
nlSpringDamperClipped(s, c, k, z, x1r, x2r),_,_ : _,_
```
Where:
* `s`: linear stiffness value
* `c`: cubic stiffness value
* `k`: upper-bound linear stiffness value
* `z`: (linear) damping value
* `x1r`: initial delayed position of mass 1
* `x2r`: initial delayed position of mass 2
#### Test
```faust
mi = library("mi.lib");
nlSpringDamperClipped_test = mi.nlSpringDamperClipped(5.0, 0.5, 8.0, 0.2, 0.0, 0.0, 0.1, -0.1);
```

---

## mi.nlPluck

------------------------`(mi.)nlPluck`----------------------
Implementation of a piecewise linear plucking interaction.
The symmetric function provides a repulsive viscoelastic interaction
upon contact, until a tipping point is reached (when the plucking occurs).
The tipping point depends both on the stiffness and the distance scaling
of the interaction.
#### Usage
```faust
nlPluck(knl, scale, z, x1r, x2r),_,_ : _,_
```
Where:
* `knl`: stiffness scaling parameter (vertical stretch of the NL function)
* `scale`: distance scaling parameter (horizontal stretch of the NL function)
* `z`: (linear) damping value
* `x1r`: initial delayed position of mass 1
* `x2r`: initial delayed position of mass 2
#### Test
```faust
mi = library("mi.lib");
nlPluck_test = mi.nlPluck(5.0, 0.1, 0.2, 0.0, 0.0, 0.05, -0.05);
```

---

## mi.nlBow

------------------------`(mi.)nlBow`----------------------
Implementation of a non-linear friction based interaction
that allows for stick-slip bowing behaviour.
Two versions are proposed : a piecewise linear function (very
similar to the `nlPluck`) or a mathematical approximation (see
Stefan Bilbao's book, Numerical Sound Synthesis).
#### Usage
```faust
nlBow(znl, scale, type, x1r, x2r),_,_ : _,_
```
Where:
* `znl`: friction scaling parameter (vertical stretch of the NL function)
* `scale`: velocity scaling parameter (horizontal stretch of the NL function)
* `type`: interaction profile (0 = piecewise linear, 1 = smooth function)
* `x1r`: initial delayed position of mass 1
* `x2r`: initial delayed position of mass 2
#### Test
```faust
mi = library("mi.lib");
nlBow_test = mi.nlBow(0.5, 0.1, 1.0, 0.0, 0.0, 0.05, -0.05);
```

---

## mi.collision

------------------------`(mi.)collision`----------------------
Implementation of a collision interaction, producing linear visco-elastic
repulsion forces when two mass elements are interpenetrating.
#### Usage
```faust
collision(k, z, thres, x1r, x2r),_,_ : _,_
```
Where:
* `k`: collision stiffness parameter
* `z`: collision damping parameter
* `thres`: threshold distance for the contact between elements
* `x1r`: initial delayed position of mass 1
* `x2r`: initial delayed position of mass 2
#### Test
```faust
mi = library("mi.lib");
collision_test = mi.collision(5.0, 0.2, 0.01, 0.0, 0.0, 0.0, -0.02);
```

---

## mi.nlCollisionClipped

------------------------`(mi.)nlCollisionClipped`----------------------
Implementation of a collision interaction, producing non-linear
visco-elastic repulsion forces when two mass elements are interpenetrating.
Bound by an upper stiffness value to maintain stability.
This interaction is particularly useful for more realistic contact dynamics
(greater difference in velocity provides sharper contacts, and reciprocally).
#### Usage
```faust
nlCollisionClipped(s, c, k, z, thres, x1r, x2r),_,_ : _,_
```
Where:
* `s`: collision linear stiffness parameter
* `c`: collision cubic stiffness parameter
* `k`: collision upper-bounding stiffness parameter
* `z`: collision damping parameter
* `thres`: threshold distance for the contact between elements
* `x1r`: initial delayed position of mass 1
* `x2r`: initial delayed position of mass 2
#### Test
```faust
mi = library("mi.lib");
nlCollisionClipped_test = mi.nlCollisionClipped(3.0, 0.5, 6.0, 0.2, 0.01, 0.0, 0.0, 0.0, -0.02);
```

---

# misceffects.lib
**Prefix:** `ef`

################################## misceffects.lib ##########################################
Miscellaneous Effects library. Its official prefix is `ef`.

This library contains a collection of diverse audio effects and utilities
not included in other specialized Faust libraries. It includes filtering, mixing, time based, pitch shifters,
and other creative or experimental signal processing components for sound design and musical applications.

The library is organized into 7 sections:

* [Dynamic](#dynamic)
* [Fibonacci](#fibonacci)
* [Filtering](#filtering)
* [Meshes](#meshes)
* [Mixing](#mixing)
* [Time Based](#time-based)
* [Pitch Shifting](#pitch-shifting)
* [Saturators](#saturators)

#### References

* <https://github.com/grame-cncm/faustlibraries/blob/master/misceffects.lib>
########################################################################################

## ef.cubicnl

---------------------`(ef.)cubicnl`-----------------------
Cubic nonlinearity distortion.
`cubicnl` is a standard Faust function.
#### Usage:
```faust
_ : cubicnl(drive,offset) : _
_ : cubicnl_nodc(drive,offset) : _
```
Where:
* `drive`: distortion amount, between 0 and 1
* `offset`: constant added before nonlinearity to give even harmonics. Note: offset
can introduce a nonzero mean - feed cubicnl output to dcblocker to remove this.
#### Test
```faust
ef = library("misceffects.lib");
os = library("oscillators.lib");
cubicnl_test = os.osc(440) : ef.cubicnl(0.5, 0.0);
cubicnl_nodc_test = os.osc(440) : ef.cubicnl_nodc(0.5, 0.0);
```
#### References
* <https://ccrma.stanford.edu/~jos/pasp/Cubic_Soft_Clipper.html>
* <https://ccrma.stanford.edu/~jos/pasp/Nonlinear_Distortion.html>

---

## ef.gate_mono

-----------------`(ef.)gate_mono`-------------------
Mono signal gate.
`gate_mono` is a standard Faust function.
#### Usage
```faust
_ : gate_mono(thresh,att,hold,rel) : _
```
Where:
* `thresh`: dB level threshold above which gate opens (e.g., -60 dB)
* `att`: attack time = time constant (sec) for gate to open (e.g., 0.0001 s = 0.1 ms)
* `hold`: hold time = time (sec) gate stays open after signal level < thresh (e.g., 0.1 s)
* `rel`: release time = time constant (sec) for gate to close (e.g., 0.020 s = 20 ms)
#### Test
```faust
ef = library("misceffects.lib");
os = library("oscillators.lib");
gate_mono_test = os.osc(440) : ef.gate_mono(-60, 0.0001, 0.1, 0.02);
```
#### References
* <http://en.wikipedia.org/wiki/Noise_gate>
* <http://www.soundonsound.com/sos/apr01/articles/advanced.asp>
* <http://en.wikipedia.org/wiki/Gating_(sound_engineering)>

---

## ef.gate_stereo

-----------------`(ef.)gate_stereo`-------------------
Stereo signal gates.
`gate_stereo` is a standard Faust function.
#### Usage
```faust
_,_ : gate_stereo(thresh,att,hold,rel) : _,_
```
Where:
* `thresh`: dB level threshold above which gate opens (e.g., -60 dB)
* `att`: attack time = time constant (sec) for gate to open (e.g., 0.0001 s = 0.1 ms)
* `hold`: hold time = time (sec) gate stays open after signal level < thresh (e.g., 0.1 s)
* `rel`: release time = time constant (sec) for gate to close (e.g., 0.020 s = 20 ms)
#### Test
```faust
ef = library("misceffects.lib");
os = library("oscillators.lib");
gate_stereo_test = os.osc(440), os.osc(441) : ef.gate_stereo(-60, 0.0001, 0.1, 0.02);
```
#### References
* <http://en.wikipedia.org/wiki/Noise_gate>
* <http://www.soundonsound.com/sos/apr01/articles/advanced.asp>
* <http://en.wikipedia.org/wiki/Gating_(sound_engineering)>

---

## ef.fibonacci

---------------`(ef.)fibonacci`---------------------------
Fibonacci system where the current output is the current
input plus the sum of the previous N outputs.
#### Usage
```faust
_ : fibonacci(N) : _
```
Where:
* `N`: the Fibonacci system's order, where 2 is standard
#### Test
```faust
ef = library("misceffects.lib");
fibonacci_test = 0 : ef.fibonacci(2);
```
#### Example
Generate the famous series: [1, 1, 2, 3, 5, 8, 13, ...]
```faust
1. : ba.impulsify : fibonacci(2)
```

---

## ef.fibonacciGeneral

---------------`(ef.)fibonacciGeneral`----------------------
Fibonacci system with customizable coefficients.
The order of the system is inferred from the number of coefficients.
#### Usage
```faust
_ : fibonacciGeneral(wave) : _
```
Where:
* `wave`: a waveform such as `waveform{1, 1}`
#### Test
```faust
ef = library("misceffects.lib");
fibonacciGeneral_test = 0 : ef.fibonacciGeneral(waveform{2, 3});
```
#### Example:
Use the update equation `y = 2*y' + 3*y'' + 4*y'''`
```faust
1. : ba.impulsify : fibonacciGeneral(waveform{2, 3, 4})
```

---

## ef.fibonacciSeq

---------------`(ef.)fibonacciSeq`---------------------------
First N numbers of the Fibonacci sequence [1, 1, 2, 3, 5, 8, ...]
as parallel channels.
#### Usage
```faust
fibonacciSeq(N) : si.bus(N)
```
Where:
* `N`: The number of Fibonacci numbers to generate as channels.
#### Test
```faust
ef = library("misceffects.lib");
fibonacciSeq_test = ef.fibonacciSeq(5);
```

---

## ef.speakerbp

-------------------------`(ef.)speakerbp`-------------------------------
Dirt-simple speaker simulator (overall bandpass eq with observed
roll-offs above and below the passband). `speakerbp` is a standard Faust function.
Low-frequency speaker model = +12 dB/octave slope breaking to
flat near f1. Implemented using two dc blockers in series.
High-frequency model = -24 dB/octave slope implemented using a
fourth-order Butterworth lowpass.
#### Usage
```faust
_ : speakerbp(f1,f2) : _
```
#### Test
```faust
ef = library("misceffects.lib");
os = library("oscillators.lib");
speakerbp_test = os.osc(440) : ef.speakerbp(100.0, 5000.0);
```
#### Example
Based on measured Celestion G12 (12" speaker):
```faust
speakerbp(130,5000)
```
TODO: perhaps this should be moved to physmodels.lib
[JOS: I don't think so because it's merely a bandpass filter tuned to speaker bandwidth]

---

## ef.piano_dispersion_filter

------------`(ef.)piano_dispersion_filter`---------------
Piano dispersion allpass filter in closed form.
#### Usage
```faust
piano_dispersion_filter(M,B,f0)
_ : piano_dispersion_filter(1,B,f0) : +(totalDelay),_ : fdelay(maxDelay) : _
```
Where:
* `M`: number of first-order allpass sections (compile-time only)
Keep below 20. 8 is typical for medium-sized piano strings.
* `B`: string inharmonicity coefficient (0.0001 is typical)
* `f0`: fundamental frequency in Hz
#### Test
```faust
ef = library("misceffects.lib");
os = library("oscillators.lib");
piano_dispersion_filter_test = os.osc(110) : ef.piano_dispersion_filter(4, 0.0001, 110);
```
#### Outputs
* MINUS the estimated delay at `f0` of allpass chain in samples,
provided in negative form to facilitate subtraction
from delay-line length.
* Output signal from allpass chain
#### References
* "Dispersion Modeling in Waveguide Piano Synthesis Using Tunable
Allpass Filters", by Jukka Rauhala and Vesa Valimaki, DAFX-2006, pp. 71-76
* <http://lib.tkk.fi/Diss/2007/isbn9789512290666/article2.pdf>
An erratum in Eq. (7) is corrected in Dr. Rauhala's encompassing
dissertation (and below).
* <http://www.acoustics.hut.fi/research/asp/piano/>
TODO: perhaps this should be moved to physmodels.lib?
[JOS: I vote yes when there is a piano model in physmodels.lib.]

---

## ef.stereo_width

-------------------------`(ef.)stereo_width`---------------------------
Stereo Width effect using the Blumlein Shuffler technique.
`stereo_width` is a standard Faust function.
#### Usage
```faust
_,_ : stereo_width(w) : _,_
```
Where:
* `w`: stereo width between 0 and 1
#### Test
```faust
ef = library("misceffects.lib");
os = library("oscillators.lib");
stereo_width_test = os.osc(440), os.osc(550) : ef.stereo_width(0.5);
```
At `w=0`, the output signal is mono ((left+right)/2 in both channels).
At `w=1`, there is no effect (original stereo image).
Thus, w between 0 and 1 varies stereo width from 0 to "original".
#### References
* "Applications of Blumlein Shuffling to Stereo Microphone Techniques"
Michael A. Gerzon, JAES vol. 42, no. 6, June 1994

---

## ef.mesh_square

----------------------------------`(ef.)mesh_square`------------------------------
Square Rectangular Digital Waveguide Mesh.
#### Usage
```faust
bus(4*N) : mesh_square(N) : bus(4*N)
```
Where:
* `N`: number of nodes along each edge - a power of two (1,2,4,8,...)
#### Test
```faust
ef = library("misceffects.lib");
mesh_square_test = (0,0,0,0) : ef.mesh_square(1);
```
#### Signal Order In and Out
The mesh is constructed recursively using 2x2 embeddings. Thus,
the top level of `mesh_square(M)` is a block 2x2 mesh, where each
block is a `mesh(M/2)`. Let these blocks be numbered 1,2,3,4 in the
geometry NW,NE,SW,SE, i.e., as:
1 2
3 4
Each block has four vector inputs and four vector outputs, where the
length of each vector is `M/2`. Label the input vectors as Ni,Ei,Wi,Si,
i.e., as the inputs from the North, East South, and West,
and similarly for the outputs. Then, for example, the upper
left input block of M/2 signals is labeled 1Ni. Most of the
connections are internal, such as 1Eo -> 2Wi. The `8*(M/2)` input
signals are grouped in the order:
1Ni 2Ni
3Si 4Si
1Wi 3Wi
2Ei 4Ei
and the output signals are:
1No 1Wo
2No 2Eo
3So 3Wo
4So 4Eo
or:
In: 1No 1Wo 2No 2Eo 3So 3Wo 4So 4Eo
Out: 1Ni 2Ni 3Si 4Si 1Wi 3Wi 2Ei 4Ei
Thus, the inputs are grouped by direction N,S,W,E, while the
outputs are grouped by block number 1,2,3,4, which can also be
interpreted as directions NW, NE, SW, SE.  A simple program
illustrating these orderings is `process = mesh_square(2);`.
#### Example
Reflectively terminated mesh impulsed at one corner:
```faust
mesh_square_test(N,x) = mesh_square(N)~(busi(4*N,x)) // input to corner
with { 
busi(N,x) = bus(N) : par(i,N,*(-1)) : par(i,N-1,_), +(x); 
};
process = 1-1' : mesh_square_test(4); // all modes excited forever
```
In this simple example, the mesh edges are connected as follows:
1No -> 1Ni, 1Wo -> 2Ni, 2No -> 3Si, 2Eo -> 4Si,
3So -> 1Wi, 3Wo -> 3Wi, 4So -> 2Ei, 4Eo -> 4Ei
A routing matrix can be used to obtain other connection geometries.
#### References
<https://ccrma.stanford.edu/~jos/pasp/Digital_Waveguide_Mesh.html>
four-port scattering junction:

---

## ef.dryWetMixer

---------------`(ef.)dryWetMixer`-------------
Linear dry-wet mixer for a N inputs and N outputs effect.
#### Usage
```faust
si.bus(inputs(FX)) : dryWetMixer(wetAmount, FX) : si.bus(inputs(FX))
```
Where:
* `wetAmount`: the wet amount (0-1). 0 produces only the dry signal and 1 produces only the wet signal
* `FX`: an arbitrary effect (N inputs and N outputs) to apply to the input bus
#### Test
```faust
ef = library("misceffects.lib");
os = library("oscillators.lib");
dryWetMixer_test = os.osc(440) : ef.dryWetMixer(0.5, fi.dcblocker);
```

---

## ef.dryWetMixerConstantPower

---------------`(ef.)dryWetMixerConstantPower`-------------
Constant-power dry-wet mixer for a N inputs and N outputs effect.
#### Usage
```faust
si.bus(inputs(FX)) : dryWetMixerConstantPower(wetAmount, FX) :si.bus(inputs(FX))
```
Where:
* `wetAmount`: the wet amount (0-1). 0 produces only the dry signal and 1 produces only the wet signal
* `FX`: an arbitrary effect (N inputs and N outputs) to apply to the input bus
#### Test
```faust
ef = library("misceffects.lib");
os = library("oscillators.lib");
dryWetMixerConstantPower_test = os.osc(440) : ef.dryWetMixerConstantPower(0.5, fi.dcblocker);
```

---

## weightsPowerLoop

------------------------`weightsPowerLoop`---------------------------
"Fan out" an index into N weights between 0 and 1. At any given
moment, two weights may be non-zero. Suppose they are N_m and N_{m+1}.
Then `cos(N_m)^2+sin(N_{m+1})^2==0.5`.
#### Usage
```faust
_ : weightsPowerLoop(N) : si.bus(N)
```
Where:
* `N`: number of output weights
* `m`: [0;N-1] (float) blend index. If m is outside [0;N-1], the behavior will loop.
.       So m=-N, m=0, and m=N should give the same output.
#### Test
```faust
ef = library("misceffects.lib");
weightsPowerLoop_test = ef.mixingEnv.weightsPowerLoop(4, 1.2);
```

---

## ef.mixLinearClamp

---------------`(ef.)mixLinearClamp`-------------------------------------------------
Linear mixer for `N` buses, each with `C` channels. The output will be a sum of 2 buses
determined by the mixing index `mix`. 0 produces the first bus, 1 produces the
second, and so on. `mix` is clamped automatically. For example, `mixLinearClamp(4, 1, 1)`
will weight its 4 inputs by `(0, 1, 0, 0)`. Similarly, `mixLinearClamp(4, 1, 1.1)`
will weight its 4 inputs by `(0,.9,.1,0)`.
#### Usage
```faust
si.bus(N*C) : mixLinearClamp(N, C, mix) : si.bus(C)
```
Where:
* `N`: the number of input buses
* `C`: the number of channels in each bus
* `mix`: the mixing index, continuous in [0;N-1].
#### Test
```faust
ef = library("misceffects.lib");
mixLinearClamp_test = (1,0,0,0) : ef.mixLinearClamp(4, 1, 1.2);
```

---

## ef.mixLinearLoop

---------------`(ef.)mixLinearLoop`-------------------------------------------------
Linear mixer for `N` buses, each with `C` channels. Refer to `mixLinearClamp`. `mix`
will loop for multiples of `N`. For example, `mixLinearLoop(4, 1, 0)` has the same
effect as `mixLinearLoop(4, 1, -4)` and `mixLinearLoop(4, 1, 4)`.
#### Usage
```faust
si.bus(N*C) : mixLinearLoop(N, C, mix) : si.bus(C)
```
Where:
* `N`: the number of input buses
* `C`: the number of channels in each bus
* `mix`: the mixing index (N-1) selects the last bus, and 0 or N selects the 0th bus.
#### Test
```faust
ef = library("misceffects.lib");
mixLinearLoop_test = (1,0,0,0) : ef.mixLinearLoop(4, 1, -0.3);
```

---

## ef.mixPowerClamp

---------------`(ef.)mixPowerClamp`-------------------------------------------------
Constant-power mixer for `N` buses, each with `C` channels. The output will be a sum of 2 buses
determined by the mixing index `mix`. 0 produces the first bus, 1 produces the
second, and so on. `mix` is clamped automatically. `mixPowerClamp(4, 1, 1)`
will weight its 4 inputs by `(0, 1./sqrt(2), 0, 0)`. Similarly, `mixPowerClamp(4, 1, 1.5)`
will weight its 4 inputs by `(0,.5,.5,0)`.
#### Usage
```faust
si.bus(N*C) : mixPowerClamp(N, C, mix) : si.bus(C)
```
Where:
* `N`: the number of input buses
* `C`: the number of channels in each bus
* `mix`: the mixing index, continuous in [0;N-1].
#### Test
```faust
ef = library("misceffects.lib");
mixPowerClamp_test = (1,0,0,0) : ef.mixPowerClamp(4, 1, 1.5);
```

---

## ef.mixPowerLoop

---------------`(ef.)mixPowerLoop`-----------------------------------------------------
Constant-power mixer for `N` buses, each with `C` channels. Refer to `mixPowerClamp`. `mix`
will loop for multiples of `N`. For example, `mixPowerLoop(4, 1, 0)` has the same effect
as `mixPowerLoop(4, 1, -4)` and `mixPowerLoop(4, 1, 4)`.
#### Usage
```faust
si.bus(N*C) : mixPowerLoop(N, C, mix) : si.bus(C)
```
Where:
* `N`: the number of input buses
* `C`: the number of channels in each bus
* `mix`: the mixing index (N-1) selects the last bus, and 0 or N selects the 0th bus.
#### Test
```faust
ef = library("misceffects.lib");
mixPowerLoop_test = (1,0,0,0) : ef.mixPowerLoop(4, 1, -0.5);
```

---

## ef.echo

----------`(ef.)echo`----------
A simple echo effect.
`echo` is a standard Faust function.
#### Usage
```faust
_ : echo(maxDuration,duration,feedback) : _
```
Where:
* `maxDuration`: the max echo duration in seconds
* `duration`: the echo duration in seconds
* `feedback`: the feedback coefficient
#### Test
```faust
ef = library("misceffects.lib");
os = library("oscillators.lib");
echo_test = os.osc(440) : ef.echo(0.5, 0.25, 0.4);
```

---

## ef.reverseEchoN

--------------------`(ef.)reverseEchoN`-------------------
Reverse echo effect.
#### Usage
```faust
_ : ef.reverseEchoN(N,delay) : si.bus(N)
```
Where:
* `N`: Number of output channels desired (1 or more), a constant numerical expression
* `delay`: echo delay (integer power of 2)
#### Test
```faust
ef = library("misceffects.lib");
os = library("oscillators.lib");
reverseEchoN_test = os.osc(440) : ef.reverseEchoN(2, 32);
```
#### Demo
```faust
_ : dm.reverseEchoN(N) : _,_
```
#### Description
The effect uses N instances of `reverseDelayRamped` at different phases.

---

## ef.reverseDelayRamped

-------------------`(ef.)reverseDelayRamped`------------------
Reverse delay with amplitude ramp.
#### Usage
```faust
_ : ef.reverseDelayRamped(delay,phase) : _
```
Where:
* `delay`: echo delay (integer power of 2)
* `phase`: float between 0 and 1 giving ramp delay phase*delay
#### Test
```faust
ef = library("misceffects.lib");
os = library("oscillators.lib");
reverseDelayRamped_test = os.osc(440) : ef.reverseDelayRamped(32, 0.6);
```
#### Demo
```faust
_ : ef.reverseDelayRamped(32,0.6) : _,_
```

---

## ef.uniformPanToStereo

-------------------`(ef.)uniformPanToStereo`------------------
Pan nChans channels to the stereo field, spread uniformly left to right.
#### Usage
```faust
si.bus(N) : ef.uniformPanToStereo(N) : _,_
```
Where:
* `N`: Number of input channels to pan down to stereo, a constant numerical expression
#### Test
```faust
ef = library("misceffects.lib");
os = library("oscillators.lib");
uniformPanToStereo_test = os.osc(440), os.osc(550), os.osc(660) : ef.uniformPanToStereo(3);
```
#### Demo
```faust
_,_,_ : ef.uniformPanToStereo(3) : _,_
```

---

## ef.tapeStop

---------------------`(ef.)tapeStop`-----------------------------------------
A tape-stop effect, like putting a finger on a vinyl record player.
#### Usage:
```faust
_,_ : tapeStop(2, LAGRANGE_ORDER, MAX_TIME_SAMP, 
crossfade, gainAlpha, stopAlpha, stopTime, stop) : _,_
```
```faust
_ : tapeStop(1, LAGRANGE_ORDER, MAX_TIME_SAMP, 
crossfade, gainAlpha, stopAlpha, stopTime, stop) : _
```
Where:
* `C`: The number of input and output channels.
* `LAGRANGE_ORDER`: The order of the Lagrange interpolation on the delay line. [2-3] recommended.
* `MAX_TIME_SAMP`: Maximum stop time in samples
* `crossfade`: A crossfade in samples to apply when resuming normal playback. Crossfade is not applied during the enabling of the tape-stop.
* `gainAlpha`: During the tape-stop, lower alpha stays louder longer. Safe values are in the range [.01,2].
* `stopAlpha`: `stopAlpha==1` represents a linear deceleration (constant force). `stopAlpha<1` represents an initially weaker, then stronger force. `stopAlpha>1` represents an initially stronger, then weaker force. Safe values are in the range [.01,2].
* `stopTime`: Desired duration of the stop time, in samples.
* `stop`: When `stop` becomes positive, the tape-stop effect will start. When `stop` becomes zero, normal audio will resume via crossfade.
#### Test
```faust
ef = library("misceffects.lib");
os = library("oscillators.lib");
tapeStop_test = os.osc(440), os.osc(441) : ef.tapeStop(2, 3, 44100, 128, 1.0, 1.0, 22050, button("stop"));
```

---

## ef.transpose

--------------`(ef.)transpose`----------------
A simple pitch shifter based on 2 delay lines.
`transpose` is a standard Faust function.
#### Usage
```faust
_ : transpose(w, x, s) : _
```
Where:
* `w`: the window length (samples)
* `x`: crossfade duration duration (samples)
* `s`: shift (semitones)
#### Test
```faust
ef = library("misceffects.lib");
os = library("oscillators.lib");
transpose_test = os.osc(440) : ef.transpose(1024, 512, 7);
```

---

## ef.softclipQuadratic

---------------`(ef.)softclipQuadratic`-------------------------------------------------
Quadratic softclip nonlinearity.
#### Usage
```faust
_ : softclipQuadratic : _
```
#### Test
```faust
ef = library("misceffects.lib");
os = library("oscillators.lib");
softclipQuadratic_test = os.osc(440) : ef.softclipQuadratic;
```
#### References
* U. Zölzer: Digital Audio Signal Processing. John Wiley & Sons Ltd, 2022.

---

## ef.wavefold

---------------`(ef.)wavefold`-------------------------------------------------
Wavefolding nonlinearity.
#### Usage
```faust
_ : wavefold(width) : _
```
Where:
* `width`: The width of the folded section [0..1] (float).
#### Test
```faust
ef = library("misceffects.lib");
os = library("oscillators.lib");
wavefold_test = os.osc(440) : ef.wavefold(0.5);
```

---

# motion.lib
**Prefix:** `mo`

################################ motion.lib ##########################################
Motion library. Its official prefix is `mo`.

This library provides helpers for motion and orientation processing: shock detection,
inclination and gravity projection, acceleration and gyroscope envelopes, orientation
weighting toward the device axes, and utilities for normalized motion streams.

Usage:

```
mo = library("motion.lib");
process = mo.shockTrigger(50, 0.75, 75, accX);
```

All motion axes are expected to be normalized to [-1, 1] (e.g., gravity ~= 1 g).
Functions return signals in [0, 1] unless documented otherwise. Time parameters
are in milliseconds unless noted. Some helpers (e.g., projectedGravity) allow an
optional dead-zone offset: low magnitudes are zeroed, and the remaining span is
rescaled to preserve the 0..1 range.

Typical use-cases:

* Map shocks to drum triggers or one-shot events.
* Derive smooth inclination or projected-gravity controls for fades/pans.
* Track acceleration/gyro envelopes to drive dynamics (filters, gains, FX sends).
* Weight device orientation toward axes for spatial routing or mode selection.
* Normalize motion streams with dead-zones to reduce jitter or false positives.

The Motion library is organized into 7 sections:

* [Shock Detection](#shock-detection)
* [Inclination and Gravity Projection](#inclination-and-gravity-projection)
* [Envelopes Helpers](#envelopes-helpers)
* [Acceleration Envelopes](#acceleration-envelopes)
* [Gyroscope Envelopes](#gyroscope-envelopes)
* [Orientation Weighting](#orientation-weighting)
* [Utility Scaling](#utility-scaling)

#### References

* <https://github.com/grame-cncm/faustlibraries/blob/master/motion.lib>
########################################################################################

## mo.shockTrigger

-----------------`(mo.)shockTrigger`--------------------
Debounced shock trigger from an accelerometer axis.
#### Usage
```faust
shockTrigger(hpHz, threshold, debounceMs, sig) : _
```
Where:
* `hpHz`: high-pass frequency (Hz) used to isolate shocks ( > 0 )
* `threshold`: trigger threshold applied after high-pass (normalized g units)
* `debounceMs`: time in milliseconds to hold the trigger high (>= 0)
* `sig`: accelerometer axis signal (normalized, typically [-1, 1])
- Output is a gate in [0, 1].
#### Example
```faust
mo = library("motion.lib");
process = mo.shockTrigger(50, 0.75, 75, accX);
```
#### Test
```faust
shockTrigger_test =
with {
mo = library("motion.lib");
os = library("oscillators.lib");
accX = os.pulsetrain(4) * 2;
} : mo.shockTrigger(50, 0.5, 50);
```

---

## mo.inclinometer

-----------------`(mo.)inclinometer`--------------------
Low-pass inclinometer for a single axis.
#### Usage
```faust
inclinometer(lpHz, sig) : _
```
Where:
* `lpHz`: low-pass frequency (Hz) ( > 0 )
* `sig`: accelerometer axis signal (normalized, typically [-1, 1])
- Output is clamped to [0, 1] with negative values removed.
#### Example
```faust
mo = library("motion.lib");
process = mo.inclinometer(1.5, accX);
```
#### Test
```faust
inclinometer_test =
with {
mo = library("motion.lib");
os = library("oscillators.lib");
} : mo.inclinometer(2, os.sawtooth(1));
```

---

## mo.inclineBalance

-----------------`(mo.)inclineBalance`--------------------
Balance between positive and negative inclination on the same axis.
#### Usage
```faust
inclineBalance(lpHz, posSig, negSig) : _
```
Where:
* `lpHz`: low-pass frequency (Hz) ( > 0 )
* `posSig`: positive-facing accelerometer axis signal (normalized, typically [-1, 1])
* `negSig`: negative-facing accelerometer axis signal (normalized, typically [-1, 1])
- Output maps posSig -> 1 and negSig -> 0 with smoothing and clamping.
#### Example
```faust
mo = library("motion.lib");
process = mo.inclineBalance(1.5, accPosX, accNegX);
```
#### Test
```faust
inclineBalance_test =
with {
mo = library("motion.lib");
os = library("oscillators.lib");
accPosX = os.sawtooth(0.1) * 0.5 + 0.5;
accNegX = accPosX * (-1);
} : mo.inclineBalance(1, accPosX, accNegX);
```

---

## mo.inclineSymmetric

-----------------`(mo.)inclineSymmetric`--------------------
Symmetric gravity comparison (0->1->0) from positive and negative axes.
#### Usage
```faust
inclineSymmetric(lpHz, posSig, negSig) : _
```
Where:
* `lpHz`: low-pass frequency (Hz) ( > 0 )
* `posSig`: positive-facing accelerometer axis signal (normalized, typically [-1, 1])
* `negSig`: negative-facing accelerometer axis signal (normalized, typically [-1, 1])
- Output peaks at 1 near either pole and returns to 0 near the midpoint.
#### Example
```faust
mo = library("motion.lib");
process = mo.inclineSymmetric(1.5, accPosX, accNegX);
```
#### Test
```faust
inclineSymmetric_test =
with {
mo = library("motion.lib");
os = library("oscillators.lib");
accPosX = os.triangle(0.2) * 0.5 + 0.5;
accNegX = accPosX * (-1);
} : mo.inclineSymmetric(2, accPosX, accNegX);
```

---

## mo.projectedGravity

-----------------`(mo.)projectedGravity`--------------------
Projects an axis onto gravity with optional dead-zone offset.
#### Usage
```faust
projectedGravity(lpHz, offset, sig) : _
```
Where:
* `lpHz`: low-pass frequency (Hz) ( > 0 )
* `offset`: dead-zone offset applied after projection (0..0.33). Magnitudes below
`offset` clamp to 0, and the remaining range is rescaled to keep the output in [0, 1].
* `sig`: accelerometer axis signal (normalized, typically [-1, 1])
- Output is normalized to [0, 1] with an optional dead zone near 0.
#### Example
```faust
mo = library("motion.lib");
process = mo.projectedGravity(1.5, 0.08, accX);
```
#### Test
```faust
projectedGravity_test =
with {
mo = library("motion.lib");
os = library("oscillators.lib");
} : mo.projectedGravity(2, 0.05, os.triangle(0.1));
```

---

## mo.motionEnvelope

-----------------`(mo.)motionEnvelope`--------------------
Base thresholded AR envelope used by the accelerometer and gyroscope helpers.
#### Usage
```faust
motionEnvelope(thr, gain, envUpMs, envDownMs, sig) : _
```
Where:
* `thr`: threshold subtracted before detection (normalized)
* `gain`: linear gain applied after thresholding
* `envUpMs`: attack time in milliseconds (>= 0)
* `envDownMs`: release time in milliseconds (>= 0)
* `sig`: input signal (normalized)
- Signal is offset by `thr`, floored at 0, scaled by `gain`, clamped to [0, 1], then
fed to an attack/release follower (`an.amp_follower_ar`).
#### Example
```faust
mo = library("motion.lib");
process = mo.motionEnvelope(0.05, 1.25, 15, 25, accX);
```

---

## mo.envelopeAbs

-----------------`(mo.)envelopeAbs`--------------------
Envelope on the absolute value of a signal (responds to both polarities).
#### Usage
```faust
envelopeAbs(thr, gain, envUpMs, envDownMs, sig) : _
```
Where:
* `thr`, `gain`, `envUpMs`, `envDownMs`: passed to `motionEnvelope`
* `sig`: input signal
- Absolute value is taken before envelope detection.

---

## mo.envelopePos

-----------------`(mo.)envelopePos`--------------------
Envelope for the positive portion of a signal.
#### Usage
```faust
envelopePos(thr, gain, envUpMs, envDownMs, sig) : _
```
Where:
* `thr`, `gain`, `envUpMs`, `envDownMs`: passed to `motionEnvelope`
* `sig`: input signal
- Negative values are ignored by the thresholding stage.

---

## mo.envelopeNeg

-----------------`(mo.)envelopeNeg`--------------------
Envelope for the negative portion of a signal (by flipping its polarity first).
#### Usage
```faust
envelopeNeg(thr, gain, envUpMs, envDownMs, sig) : _
```
Where:
* `thr`, `gain`, `envUpMs`, `envDownMs`: passed to `motionEnvelope`
* `sig`: input signal
- The signal is negated before the shared positive-only detector.

---

## mo.pita3

-----------------`(mo.)pita3`--------------------
3D magnitude helper `sqrt(x^2 + y^2 + z^2)` used for total envelopes.
#### Usage
```faust
pita3(x, y, z) : _
```

---

## mo.totalEnvelope

-----------------`(mo.)totalEnvelope`--------------------
Magnitude-based envelope across three axes.
#### Usage
```faust
totalEnvelope(thr, gain, envUpMs, envDownMs, x, y, z) : _
```
Where:
* `thr`, `gain`, `envUpMs`, `envDownMs`: passed to `motionEnvelope`
* `x`, `y`, `z`: three-axis signals (normalized)
- Computes a magnitude via `pita3` then applies `motionEnvelope`.

---

## mo.accelEnvelopeAbs

-----------------`(mo.)accelEnvelopeAbs`--------------------
Envelope follower on the absolute value of an accelerometer axis.
#### Usage
```faust
accelEnvelopeAbs(thr, gain, envUpMs, envDownMs, sig) : _
```
Where:
* `thr`: threshold subtracted before detection (normalized)
* `gain`: linear gain applied after thresholding
* `envUpMs`: attack time in milliseconds (>= 0)
* `envDownMs`: release time in milliseconds (>= 0)
* `sig`: accelerometer axis signal (normalized, typically [-1, 1])
- Output envelope is clamped to [0, 1].
#### Example
```faust
mo = library("motion.lib");
process = mo.accelEnvelopeAbs(0.1, 1.2, 10, 12, accX);
```
#### Test
```faust
accelEnvelopeAbs_test =
with {
mo = library("motion.lib");
os = library("oscillators.lib");
accX = os.sawtooth(0.5);
} : mo.accelEnvelopeAbs(0.1, 1.5, 5, 20, accX);
```

---

## mo.accelEnvelopePos

-----------------`(mo.)accelEnvelopePos`--------------------
Envelope follower for positive acceleration on one axis.
#### Usage
```faust
accelEnvelopePos(thr, gain, envUpMs, envDownMs, sig) : _
```
Where:
* `thr`: threshold subtracted before detection (normalized)
* `gain`: linear gain applied after thresholding
* `envUpMs`: attack time in milliseconds (>= 0)
* `envDownMs`: release time in milliseconds (>= 0)
* `sig`: accelerometer axis signal (normalized, typically [-1, 1])
- Negative values are ignored; output envelope is clamped to [0, 1].
#### Example
```faust
mo = library("motion.lib");
process = mo.accelEnvelopePos(0.05, 1.35, 10, 10, accX);
```
#### Test
```faust
accelEnvelopePos_test =
with {
mo = library("motion.lib");
os = library("oscillators.lib");
} : mo.accelEnvelopePos(0.05, 1, 5, 5, os.triangle(0.25));
```

---

## mo.accelEnvelopeNeg

-----------------`(mo.)accelEnvelopeNeg`--------------------
Envelope follower for negative acceleration on one axis.
#### Usage
```faust
accelEnvelopeNeg(thr, gain, envUpMs, envDownMs, sig) : _
```
Where:
* `thr`: threshold subtracted before detection (normalized)
* `gain`: linear gain applied after thresholding
* `envUpMs`: attack time in milliseconds (>= 0)
* `envDownMs`: release time in milliseconds (>= 0)
* `sig`: accelerometer axis signal (normalized, typically [-1, 1])
- Positive values are ignored; output envelope is clamped to [0, 1].
#### Example
```faust
mo = library("motion.lib");
process = mo.accelEnvelopeNeg(0.05, 1.35, 10, 10, accX);
```
#### Test
```faust
accelEnvelopeNeg_test =
with {
mo = library("motion.lib");
os = library("oscillators.lib");
} : mo.accelEnvelopeNeg(0.05, 1, 5, 5, os.triangle(0.25));
```

---

## mo.totalAccel

-----------------`(mo.)totalAccel`--------------------
Total acceleration magnitude with thresholding and envelope.
#### Usage
```faust
totalAccel(thr, gain, envUpMs, envDownMs, ax, ay, az) : _
```
Where:
* `thr`: threshold subtracted before detection (normalized)
* `gain`: linear gain applied after thresholding
* `envUpMs`: attack time in milliseconds (>= 0)
* `envDownMs`: release time in milliseconds (>= 0)
* `ax`: accelerometer X axis (normalized, typically [-1, 1])
* `ay`: accelerometer Y axis (normalized, typically [-1, 1])
* `az`: accelerometer Z axis (normalized, typically [-1, 1])
- Output magnitude is clamped to [0, 1].
#### Example
```faust
mo = library("motion.lib");
process = mo.totalAccel(0.1, 1.35, 10, 10, ax, ay, az);
```
#### Test
```faust
totalAccel_test =
with {
mo = library("motion.lib");
os = library("oscillators.lib");
ax = os.sawtooth(0.2) * 0.2;
ay = os.triangle(0.15) * 0.1;
az = os.sawtooth(0.12) * 0.3;
} : mo.totalAccel(0.05, 1.2, 8, 12, ax, ay, az);
```

---

## mo.gyroEnvelopeAbs

-----------------`(mo.)gyroEnvelopeAbs`--------------------
Envelope follower on the absolute value of a gyroscope axis.
#### Usage
```faust
gyroEnvelopeAbs(thr, gain, envUpMs, envDownMs, sig) : _
```
Where:
* `thr`: threshold subtracted before detection (normalized)
* `gain`: linear gain applied after thresholding
* `envUpMs`: attack time in milliseconds (>= 0)
* `envDownMs`: release time in milliseconds (>= 0)
* `sig`: gyroscope axis signal (normalized rad/s range)
- Output envelope is clamped to [0, 1].
#### Example
```faust
mo = library("motion.lib");
process = mo.gyroEnvelopeAbs(0.01, 0.8, 50, 50, gx);
```
#### Test
```faust
gyroEnvelopeAbs_test =
with {
mo = library("motion.lib");
os = library("oscillators.lib");
} : mo.gyroEnvelopeAbs(0.02, 0.9, 25, 30, os.sawtooth(0.5));
```

---

## mo.gyroEnvelopePos

-----------------`(mo.)gyroEnvelopePos`--------------------
Envelope follower for positive gyroscope rotation on one axis.
#### Usage
```faust
gyroEnvelopePos(thr, gain, envUpMs, envDownMs, sig) : _
```
Where:
* `thr`: threshold subtracted before detection (normalized)
* `gain`: linear gain applied after thresholding
* `envUpMs`: attack time in milliseconds (>= 0)
* `envDownMs`: release time in milliseconds (>= 0)
* `sig`: gyroscope axis signal (normalized rad/s range)
- Negative values are ignored; output envelope is clamped to [0, 1].
#### Example
```faust
mo = library("motion.lib");
process = mo.gyroEnvelopePos(0.01, 0.8, 50, 50, gx);
```
#### Test
```faust
gyroEnvelopePos_test =
with {
mo = library("motion.lib");
os = library("oscillators.lib");
} : mo.gyroEnvelopePos(0.02, 0.9, 25, 30, os.triangle(0.5));
```

---

## mo.gyroEnvelopeNeg

-----------------`(mo.)gyroEnvelopeNeg`--------------------
Envelope follower for negative gyroscope rotation on one axis.
#### Usage
```faust
gyroEnvelopeNeg(thr, gain, envUpMs, envDownMs, sig) : _
```
Where:
* `thr`: threshold subtracted before detection (normalized)
* `gain`: linear gain applied after thresholding
* `envUpMs`: attack time in milliseconds (>= 0)
* `envDownMs`: release time in milliseconds (>= 0)
* `sig`: gyroscope axis signal (normalized rad/s range)
- Positive values are ignored; output envelope is clamped to [0, 1].
#### Example
```faust
mo = library("motion.lib");
process = mo.gyroEnvelopeNeg(0.01, 0.8, 50, 50, gx);
```
#### Test
```faust
gyroEnvelopeNeg_test =
with {
mo = library("motion.lib");
os = library("oscillators.lib");
} : mo.gyroEnvelopeNeg(0.02, 0.9, 25, 30, os.triangle(0.5));
```

---

## mo.totalGyro

-----------------`(mo.)totalGyro`--------------------
Total gyroscope magnitude with thresholding and envelope.
#### Usage
```faust
totalGyro(thr, gain, envUpMs, envDownMs, gx, gy, gz) : _
```
Where:
* `thr`: threshold subtracted before detection (normalized)
* `gain`: linear gain applied after thresholding
* `envUpMs`: attack time in milliseconds (>= 0)
* `envDownMs`: release time in milliseconds (>= 0)
* `gx`: gyroscope X axis (normalized rad/s range)
* `gy`: gyroscope Y axis (normalized rad/s range)
* `gz`: gyroscope Z axis (normalized rad/s range)
- Output magnitude is clamped to [0, 1].
#### Example
```faust
mo = library("motion.lib");
process = mo.totalGyro(0.01, 0.8, 50, 50, gx, gy, gz);
```
#### Test
```faust
totalGyro_test =
with {
mo = library("motion.lib");
os = library("oscillators.lib");
gx = os.sawtooth(0.2) * 0.2;
gy = os.triangle(0.15) * 0.1;
gz = os.sawtooth(0.12) * 0.3;
} : mo.totalGyro(0.01, 0.9, 25, 30, gx, gy, gz);
```

---

## mo.orientationWeight

-----------------`(mo.)orientationWeight`--------------------
Weighting of a 3D vector toward a target axis with shape and smoothing.
#### Usage
```faust
orientationWeight(targetX, targetY, targetZ, shape, xs, ys, zs, smoothMs) : _
```
Where:
* `targetX`: target X coordinate (-1..1)
* `targetY`: target Y coordinate (-1..1)
* `targetZ`: target Z coordinate (-1..1)
* `shape`: scaling applied to the distance (>= 0, larger tightens the lobe)
* `xs`: current X coordinate (normalized)
* `ys`: current Y coordinate (normalized)
* `zs`: current Z coordinate (normalized)
* `smoothMs`: smoothing time in milliseconds (>= 0)
- Output weight is clamped to [0, 1].
#### Example
```faust
mo = library("motion.lib");
process = mo.orientationWeight(0, 1, 0, 1, x, y, z, 10);
```
#### Test
```faust
orientationWeight_test =
with {
mo = library("motion.lib");
os = library("oscillators.lib");
x = os.triangle(0.1);
y = os.sawtooth(0.1);
z = os.triangle(0.05);
} : mo.orientationWeight(0, 1, 0, 1, x, y, z, 10);
```

---

## mo.orientation6

-----------------`(mo.)orientation6`--------------------
Weights toward the six device axes (Cour/stage left -X, Rear -Y, Jardin/stage right +X,
Front +Y, Down -Z, Up +Z).
#### Usage
```faust
orientation6(xs, ys, zs,
shapeCour, shapeRear, shapeJardin, shapeFront, shapeDown, shapeUp,
smoothMs) : _
```
Where:
* `xs`: current X coordinate (normalized)
* `ys`: current Y coordinate (normalized)
* `zs`: current Z coordinate (normalized)
* `shapeCour`: shape for Cour (-X)
* `shapeRear`: shape for Rear (-Y)
* `shapeJardin`: shape for Jardin (+X)
* `shapeFront`: shape for Front (+Y)
* `shapeDown`: shape for Down (-Z)
* `shapeUp`: shape for Up (+Z)
* `smoothMs`: smoothing time in milliseconds (>= 0)
- Output is six weights (Cour, Rear, Jardin, Front, Down, Up), each in [0, 1].
#### Example
```faust
mo = library("motion.lib");
process = mo.orientation6(x, y, z, 1, 1, 1, 1, 1, 1, 10);
```
#### Test
```faust
orientation6_test =
with {
mo = library("motion.lib");
os = library("oscillators.lib");
x = os.triangle(0.05);
y = os.sawtooth(0.08);
z = os.triangle(0.03);
} : mo.orientation6(x, y, z, 1, 1, 1, 1, 1, 1, 10);
```

---

## mo.scale

-----------------`(mo.)scale`--------------------
Normalized scaler with input dead-zone and bounded output range.
#### Usage
```faust
scale(ilow, ihigh, olow, ohigh) : _
```
Where:
* `ilow`: minimum input value before scaling starts (0..1)
* `ihigh`: maximum input value before clamping (must be > ilow)
* `olow`: minimum output value
* `ohigh`: maximum output value
- Inputs below ilow clamp to olow; above ihigh clamp to ohigh.
#### Example
```faust
mo = library("motion.lib");
process = _ : mo.scale(0.2, 0.8, 100, 20000) : _;
```
#### Test
```faust
scale_test =
with {
mo = library("motion.lib");
os = library("oscillators.lib");
} : os.sawtooth(0.2) : mo.scale(0.2, 0.8, 0, 1);
```

---

# noises.lib
**Prefix:** `no`

################################ noises.lib ##########################################
Noises library. Its official prefix is `no`.

This library provides various noise generators and stochastic signal sources
for audio synthesis and testing. It includes white, pink, brown, and blue noise,
as well as pseudo-random number generators and utilities for decorrelated signals
and random modulation in Faust DSP programs.

The Noises library is organized into 1 section:

* [Functions Reference](#functions-reference)

#### References

* <https://github.com/grame-cncm/faustlibraries/blob/master/noises.lib>
########################################################################################

## no.noise

-------`(no.)noise`----------
White noise generator (outputs random number between -1 and 1).
`noise` is a standard Faust function.
#### Usage
```faust
noise : _
```
Where:
* output: white noise signal in [-1, 1].
#### Test
```faust
no = library("noises.lib");
noise_test = no.noise;
```

---

## no.multirandom

---------------------`(no.)multirandom`--------------------------
Generates multiple decorrelated random numbers in parallel.
#### Usage
```faust
multirandom(N) : si.bus(N)
```
Where:
* `N`: the number of decorrelated random numbers in parallel, a constant numerical expression
#### Test
```faust
no = library("noises.lib");
multirandom_test = no.multirandom(4);
```

---

## no.multinoise

-----------------------`(no.)multinoise`------------------------
Generates multiple decorrelated noises in parallel.
#### Usage
```faust
multinoise(N) : si.bus(N)
```
Where:
* `N`: the number of decorrelated random numbers in parallel, a constant numerical expression
#### Test
```faust
no = library("noises.lib");
multinoise_test = no.multinoise(3);
```

---

## no.noises

-----------------------`(no.)noises`------------------------
A convenient wrapper around multinoise.
#### Usage
```faust
noises(N,i) : _
```
Where:
* `N`: the number of decorrelated random numbers in parallel, a constant numerical expression
* `i`: the selected random number (i in [0..N[)
#### Test
```faust
no = library("noises.lib");
noises_test = no.noises(4, 2);
```

---

## no.dnoise

-----------------------`(no.)dnoise`------------------------
A deterministic noise burst with a dynamically adjustable seed, enabling consistent recall.
Useful for noise variation sensitive applications like replicable/recallable percussion sounds and waveguide excitation.
#### Usage
```faust
dnoise(t,sx) : _
```
Where:
* `t`: is a noise burst trigger
* `sx`: defines the range of integer seed multipliers.
#### Test
```faust
no = library("noises.lib");
ba = library("basics.lib");
dnoise_test = (1 : ba.impulsify, 10.0) : no.dnoise;
```
#### Example
This expression `sx = hslider("seed multiplier",1,1,1000,1)` allows 1000 distinct seed variations.
To generate a burst with a fixed length, use `ba.spulse(bLength, t)` (as trigger for the `t` parameter), where `bLength` is the burst duration in samples and `t` is a trigger.

---

## no.randomseed

-----------------------`(no.)randomseed`------------------------
A random seed based on the foreign function `arc4random`
(see man arc4random). Used in `rnoise`, `rmultirandom`, etc. to
avoid having the same pseudo random sequence at each run.
WARNING: using the foreign function `arc4random`, so only available in C/C++ and LLVM backends.
#### Usage
```faust
randomseed : _
```
Where:
* output: platform-specific random seed value.
#### Test
```faust
no = library("noises.lib");
randomseed_test = no.randomseed;
```

---

## no.rnoise

-----------------------`(no.)rnoise`-----------------------
A randomized white noise generator (outputs random number between -1 and 1).
WARNING: using the foreign function `arc4random`, so only available in C/C++ and LLVM backends.
#### Usage
```faust
rnoise : _
```
#### Test
```faust
no = library("noises.lib");
rnoise_test = no.rnoise;
```

---

## no.rmultirandom

---------------------`(no.)rmultirandom`--------------------------
Generates multiple decorrelated random numbers in parallel.
WARNING: using the foreign function `arc4random`, so only available in C/C++ and LLVM backends.
#### Usage
```faust
rmultirandom(N) : _
```
Where:
* `N`: the number of decorrelated random numbers in parallel, a constant numerical expression
#### Test
```faust
no = library("noises.lib");
rmultirandom_test = no.rmultirandom(4);
```

---

## no.rmultinoise

-----------------------`(no.)rmultinoise`------------------------
Generates multiple decorrelated noises in parallel.
WARNING: using the foreign function `arc4random`, so only available in C/C++ and LLVM backends.
#### Usage
```faust
rmultinoise(N) : _
```
Where:
* `N`: the number of decorrelated random numbers in parallel, a constant numerical expression
#### Test
```faust
no = library("noises.lib");
rmultinoise_test = no.rmultinoise(3);
```

---

## no.rnoises

-----------------------`(no.)rnoises`------------------------
A convenient wrapper around rmultinoise.
WARNING: using the foreign function `arc4random`, so only available in C/C++ and LLVM backends.
#### Usage
```faust
rnoises(N,i) : _
```
Where:
* `N`: the number of decorrelated random numbers in parallel
* `i`: the selected random number (i in [0..N[)
#### Test
```faust
no = library("noises.lib");
rnoises_test = no.rnoises(4, 2);
```

---

## no.pink_noise

---------------------------`(no.)pink_noise`--------------------------
Pink noise (1/f noise) generator (third-order approximation covering the audio band well).
`pink_noise` is a standard Faust function.
#### Usage
```faust
pink_noise : _
```
Where:
* output: pink (1/f) noise signal.
#### Test
```faust
no = library("noises.lib");
pink_noise_test = no.pink_noise;
```
#### Alternatives
Higher-order approximations covering any frequency band can be obtained using
```faust
no.noise : fi.spectral_tilt(order,lowerBandLimit,Bandwidth,p)
```
where `p=-0.5` means filter rolloff `f^(-1/2)` which gives 1/f rolloff in the
power spectral density, and can be changed to other real values.
#### Example
pink_noise_compare.dsp - compare three pinking filters
```faust
process = pink_noises with {
f0 = 35; // Lower bandlimit in Hz
bw3 = 0.7 * ma.SR/2.0 - f0; // Bandwidth in Hz, 3rd order case
bw9 = 0.8 * ma.SR/2.0 - f0; // Bandwidth in Hz, 9th order case
pink_tilt_3 = fi.spectral_tilt(3,f0,bw3,-0.5);
pink_tilt_9 = fi.spectral_tilt(9,f0,bw9,-0.5);
pink_noises = 1-1' <:
no.pink_filter, // original designed by invfreqz in Octave
pink_tilt_3,    // newer method using the same filter order
pink_tilt_9;    // newer method using a higher filter order
};
```
#### Output of Example
```faust
faust2octave pink_noise_compare.dsp
Octave:1> semilogx(20*log10(abs(fft(faustout,8192))(1:4096,:)));
...
```
<img alt="pink_noise_demo figure" src="https://ccrma.stanford.edu/wiki/Images/8/86/Tpinkd.jpg" width="600" />
#### References
* <https://ccrma.stanford.edu/~jos/sasp/Example_Synthesis_1_F_Noise.html>

---

## no.pink_noise_vm

-------------------------`(no.)pink_noise_vm`-------------------
Multi pink noise generator.
#### Usage
```faust
pink_noise_vm(N) : _
```
Where:
* `N`: number of latched white-noise processes to sum,
not to exceed sizeof(int) in C++ (typically 32).
#### Test
```faust
no = library("noises.lib");
pink_noise_vm_test = no.pink_noise_vm(4);
```
#### References
* <http://www.dsprelated.com/showarticle/908.php>
* <http://www.firstpr.com.au/dsp/pink-noise/#Voss-McCartney>

---

## no.sparse_noise

-------------------------`(no.)sparse_noise`-------------------
Sparse noise generator.
#### Usage
```faust
sparse_noise(f0) : _
```
Where:
* `f0`: average frequency of noise impulses per second
Random impulses in the amplitude range -1 to 1 are generated
at an average rate of f0 impulses per second.
#### Test
```faust
no = library("noises.lib");
sparse_noise_test = no.sparse_noise(5.0);
```
#### References
* See velvet_noise

---

## no.velvet_noise_vm

-------------------------`(no.)velvet_noise_vm`-------------------
Velvet noise generator.
#### Usage
```faust
velvet_noise(amp, f0) : _
```
Where:
* `amp`: amplitude of noise impulses (positive and negative)
* `f0`: average frequency of noise impulses per second
#### Test
```faust
no = library("noises.lib");
velvet_noise_test = no.velvet_noise(0.5, 5.0);
```
#### References
* Matti Karjalainen and Hanna Jarvelainen,
"Reverberation Modeling Using Velvet Noise",
in Proc. 30th Int. Conf. Intelligent Audio Environments (AES07),
March 2007.

---

## no.gnoise

----------------------------`(no.)gnoise`------------------------
Approximate zero-mean, unit-variance Gaussian white noise generator.
#### Usage
```faust
gnoise(N) : _
```
Where:
* `N`: number of uniform random numbers added to approximate Gaussian white noise
#### Test
```faust
no = library("noises.lib");
gnoise_test = no.gnoise(8);
```
#### References
* See Central Limit Theorem

---

## no.colored_noise

-----------------`(no.)colored_noise`--------------------
Generates a colored noise signal with an arbitrary spectral
roll-off factor (alpha) over the entire audible frequency range
(20-20000 Hz). The output is normalized so that an equal RMS
level is maintained for different values of alpha.
#### Usage
```faust
colored_noise(N,alpha) : _
```
Where:
* `N`: desired integer filter order (constant numerical expression)
* `alpha`: slope of roll-off, between -1 and 1. -1 corresponds to
brown/red noise, -1/2 pink noise, 0 white noise, 1/2 blue noise,
and 1 violet/azure noise.
#### Test
```faust
no = library("noises.lib");
colored_noise_test = no.colored_noise(4, 0.0);
```
#### Examples
See `dm.colored_noise_demo`.

---

# oscillators.lib
**Prefix:** `os`

############################## oscillators.lib ######################################
Oscillators library. Its official prefix is `os`.

This library provides a wide range of oscillator designs for sound synthesis.
It includes classic waveforms (sine, sawtooth, square, triangle), band-limited and anti-aliased
oscillators, phase and frequency modulation units, as well as noise-based and physical-model
driven oscillators for advanced synthesis techniques in Faust.

The oscillators library is organized into 9 sections:

* [Wave-Table-Based Oscillators](#wave-table-based-oscillators)
* [Low Frequency Oscillators](#low-frequency-oscillators)
* [Low Frequency Sawtooths](#low-frequency-sawtooths)
* [Alias-Suppressed Sawtooth](#alias-suppressed-sawtooth)
* [Alias-Suppressed Pulse, Square, and Impulse Trains](#alias-suppressed-pulse-square-and-impulse-trains)
* [Filter-Based Oscillators](#filter-based-oscillators)
* [Waveguide-Resonator-Based Oscillators](#waveguide-resonator-based-oscillators)
* [Casio CZ Oscillators](#casio-cz-oscillators)
* [PolyBLEP-Based Oscillators](#polyblep-based-oscillators)

#### References

* <https://github.com/grame-cncm/faustlibraries/blob/master/oscillators.lib>
########################################################################################

## os.sinwaveform

-----------------------`(os.)sinwaveform`------------------------
Sine waveform ready to use with a `rdtable`.
#### Usage
```faust
sinwaveform(tablesize) : _
```
Where:
* `tablesize`: the table size
#### Test
```faust
os = library("oscillators.lib");
sinwaveform_test = os.sinwaveform(1024);
```

---

## os.coswaveform

-----------------------`(os.)coswaveform`------------------------
Cosine waveform ready to use with a `rdtable`.
#### Usage
```faust
coswaveform(tablesize) : _
```
Where:
* `tablesize`: the table size
#### Test
```faust
os = library("oscillators.lib");
coswaveform_test = os.coswaveform(1024);
```

---

## os.phasor

-----------------------`(os.)phasor`------------------------
A simple phasor to be used with a `rdtable`.
`phasor` is a standard Faust function.
#### Usage
```faust
phasor(tablesize,freq) : _
```
Where:
* `tablesize`: the table size
* `freq`: the frequency in Hz
Note that `tablesize` is just a multiplier for the output of a unit-amp phasor
so `phasor(1.0, freq)` can be used to generate a phasor output in the range [0, 1[.
#### Test
```faust
os = library("oscillators.lib");
phasor_test = os.phasor(1024, 440);
```

---

## os.hs_phasor

-----------------------`(os.)hs_phasor`------------------------
Hardsyncing phasor to be used with a `rdtable`.
#### Usage
```faust
hs_phasor(tablesize,freq,reset) :  _
```
Where:
* `tablesize`: the table size
* `freq`: the frequency in Hz
* `reset`: a reset signal, reset phase to 0 when equal to 1
#### Test
```faust
os = library("oscillators.lib");
hs_phasor_test = os.hs_phasor(1024, 330, button("reset"));
```

---

## os.hsp_phasor

-----------------------`(os.)hsp_phasor`------------------------
Hardsyncing phasor with selectable phase to be used with a `rdtable`.
#### Usage
```faust
hsp_phasor(tablesize,freq,reset,phase)
```
Where:
* `tablesize`: the table size
* `freq`: the frequency in Hz
* `reset`: reset the oscillator to phase when equal to 1
* `phase`: phase between 0 and 1
#### Test
```faust
os = library("oscillators.lib");
hsp_phasor_test = os.hsp_phasor(1024, 330, button("reset"), 0.25);
```

---

## os.oscsin

-----------------------`(os.)oscsin`------------------------
Sine wave oscillator.
`oscsin` is a standard Faust function.
#### Usage
```faust
oscsin(freq) : _
```
Where:
* `freq`: the frequency in Hz
#### Test
```faust
os = library("oscillators.lib");
oscsin_test = os.oscsin(440);
```

---

## os.hs_oscsin

-----------------------`(os.)hs_oscsin`------------------------
Sin lookup table with hardsyncing phase.
#### Usage
```faust
hs_oscsin(freq,reset) : _
```
Where:
* `freq`: the frequency in Hz
* `reset`: reset the oscillator to 0 when equal to 1
#### Test
```faust
os = library("oscillators.lib");
hs_oscsin_test = os.hs_oscsin(440, button("reset"));
```

---

## os.osccos

-----------------------`(os.)osccos`------------------------
Cosine wave oscillator.
#### Usage
```faust
osccos(freq) : _
```
Where:
* `freq`: the frequency in Hz
#### Test
```faust
os = library("oscillators.lib");
osccos_test = os.osccos(440);
```

---

## os.hs_osccos

-----------------------`(os.)hs_osccos`------------------------
Cos lookup table with hardsyncing phase.
#### Usage
```faust
hs_osccos(freq,reset) : _
```
Where:
* `freq`: the frequency in Hz
* `reset`: reset the oscillator to 0 when equal to 1
#### Test
```faust
os = library("oscillators.lib");
hs_osccos_test = os.hs_osccos(440, button("reset"));
```

---

## os.oscp

-----------------------`(os.)oscp`------------------------
A sine wave generator with controllable phase.
#### Usage
```faust
oscp(freq,phase) : _
```
Where:
* `freq`: the frequency in Hz
* `phase`: the phase in radian
#### Test
```faust
os = library("oscillators.lib");
ma = library("maths.lib");
oscp_test = os.oscp(440, ma.PI/3);
```

---

## os.osci

-----------------------`(os.)osci`------------------------
Interpolated phase sine wave oscillator.
#### Usage
```faust
osci(freq) : _
```
Where:
* `freq`: the frequency in Hz
#### Test
```faust
os = library("oscillators.lib");
osci_test = os.osci(440);
```

---

## os.osc

-----------------------`(os.)osc`------------------------
Default sine wave oscillator (same as [oscsin](#oscsin)).
`osc` is a standard Faust function.
#### Usage
```faust
osc(freq) : _
```
Where:
* `freq`: the frequency in Hz
#### Test
```faust
os = library("oscillators.lib");
osc_test = os.osc(440);
```

---

## os.m_oscsin

-----------------------`(os.)m_oscsin`------------------------
Sine wave oscillator based on the `sin` mathematical function.
#### Usage
```faust
m_oscsin(freq) : _
```
Where:
* `freq`: the frequency in Hz
#### Test
```faust
os = library("oscillators.lib");
m_oscsin_test = os.m_oscsin(440);
```

---

## os.m_osccos

-----------------------`(os.)m_osccos`------------------------
Sine wave oscillator based on the `cos` mathematical function.
#### Usage
```faust
m_osccos(freq) : _
```
Where:
* `freq`: the frequency in Hz
#### Test
```faust
os = library("oscillators.lib");
m_osccos_test = os.m_osccos(440);
```

---

## os.lf_imptrain

--------`(os.)lf_imptrain`----------
Unit-amplitude low-frequency impulse train.
`lf_imptrain` is a standard Faust function.
#### Usage
```faust
lf_imptrain(freq) : _
```
Where:
* `freq`: frequency in Hz
#### Test
```faust
os = library("oscillators.lib");
lf_imptrain_test = os.lf_imptrain(3);
```

---

## os.lf_pulsetrainpos

--------`(os.)lf_pulsetrainpos`----------
Unit-amplitude nonnegative LF pulse train, duty cycle between 0 and 1.
#### Usage
```faust
lf_pulsetrainpos(freq, duty) : _
```
Where:
* `freq`: frequency in Hz
* `duty`: duty cycle between 0 and 1
#### Test
```faust
os = library("oscillators.lib");
lf_pulsetrainpos_test = os.lf_pulsetrainpos(3, 0.35);
```

---

## os.lf_pulsetrain

--------`(os.)lf_pulsetrain`----------
Unit-amplitude zero-mean LF pulse train, duty cycle between 0 and 1.
#### Usage
```faust
lf_pulsetrain(freq,duty) : _
```
Where:
* `freq`: frequency in Hz
* `duty`: duty cycle between 0 and 1
#### Test
```faust
os = library("oscillators.lib");
lf_pulsetrain_test = os.lf_pulsetrain(3, 0.35);
```

---

## os.lf_squarewavepos

--------`(os.)lf_squarewavepos`----------
Positive LF square wave in [0,1]
#### Usage
```faust
lf_squarewavepos(freq) : _
```
Where:
* `freq`: frequency in Hz
#### Test
```faust
os = library("oscillators.lib");
lf_squarewavepos_test = os.lf_squarewavepos(3);
```

---

## os.lf_squarewave

--------`(os.)lf_squarewave`----------
Zero-mean unit-amplitude LF square wave.
`lf_squarewave` is a standard Faust function.
#### Usage
```faust
lf_squarewave(freq) : _
```
Where:
* `freq`: frequency in Hz
#### Test
```faust
os = library("oscillators.lib");
lf_squarewave_test = os.lf_squarewave(3);
```

---

## os.lf_trianglepos

--------`(os.)lf_trianglepos`----------
Positive unit-amplitude LF positive triangle wave.
#### Usage
```faust
lf_trianglepos(freq) : _
```
Where:
* `freq`: frequency in Hz
#### Test
```faust
os = library("oscillators.lib");
lf_trianglepos_test = os.lf_trianglepos(3);
```

---

## os.lf_triangle

----------`(os.)lf_triangle`----------
Zero-mean unit-amplitude LF triangle wave.
`lf_triangle` is a standard Faust function.
#### Usage
```faust
lf_triangle(freq) : _
```
Where:
* `freq`: frequency in Hz
#### Test
```faust
os = library("oscillators.lib");
lf_triangle_test = os.lf_triangle(3);
```

---

## os.lf_rawsaw

-----------------`(os.)lf_rawsaw`--------------------
Simple sawtooth waveform oscillator between 0 and period in samples.
#### Usage
```faust
lf_rawsaw(periodsamps) : _
```
Where:
* `periodsamps`: number of periods per samples
#### Test
```faust
os = library("oscillators.lib");
lf_rawsaw_test = os.lf_rawsaw(128);
```

---

## os.lf_sawpos

-----------------`(os.)lf_sawpos`--------------------
Simple sawtooth waveform oscillator between 0 and 1.
#### Usage
```faust
lf_sawpos(freq) : _
```
Where:
* `freq`: frequency in Hz
#### Test
```faust
os = library("oscillators.lib");
lf_sawpos_test = os.lf_sawpos(3);
```

---

## os.lf_sawpos_phase

-----------------`(os.)lf_sawpos_phase`--------------------
Simple sawtooth waveform oscillator between 0 and 1
with phase control.
#### Usage
```faust
lf_sawpos_phase(freq, phase) : _
```
Where:
* `freq`: frequency in Hz
* `phase`: phase between 0 and 1
#### Test
```faust
os = library("oscillators.lib");
lf_sawpos_phase_test = os.lf_sawpos_phase(3, 0.25);
```

---

## os.lf_sawpos_reset

-----------------`(os.)lf_sawpos_reset`--------------------
Simple sawtooth waveform oscillator between 0 and 1
with reset.
#### Usage
```faust
lf_sawpos_reset(freq,reset) : _
```
Where:
* `freq`: frequency in Hz
* `reset`: reset the oscillator to 0 when equal to 1
#### Test
```faust
os = library("oscillators.lib");
lf_sawpos_reset_test = os.lf_sawpos_reset(3, button("reset"));
```

---

## os.lf_sawpos_phase_reset

-----------------`(os.)lf_sawpos_phase_reset`--------------------
Simple sawtooth waveform oscillator between 0 and 1
with phase control and reset.
#### Usage
```faust
lf_sawpos_phase_reset(freq,phase,reset) : _
```
Where:
* `freq`: frequency in Hz
* `phase`: phase between 0 and 1
* `reset`: reset the oscillator to phase when equal to 1
#### Test
```faust
os = library("oscillators.lib");
lf_sawpos_phase_reset_test = os.lf_sawpos_phase_reset(3, 0.75, button("reset"));
```

---

## os.lf_saw

-----------------`(os.)lf_saw`--------------------
Simple sawtooth waveform oscillator between -1 and 1.
`lf_saw` is a standard Faust function.
#### Usage
```faust
lf_saw(freq) : _
```
Where:
* `freq`: frequency in Hz
#### Test
```faust
os = library("oscillators.lib");
lf_saw_test = os.lf_saw(3);
```

---

## os.sawN

-----------------`(os.)sawN`--------------------
Alias-Suppressed Sawtooth Audio-Frequency Oscillator using Nth-order polynomial transitions
to reduce aliasing.
`sawN(N,freq)`, `sawNp(N,freq,phase)`, `saw2dpw(freq)`, `saw2(freq)`, `saw3(freq)`,
`saw4(freq)`, `sawtooth(freq)`, `saw2f2(freq)`, `saw2f4(freq)`
#### Usage
```faust
sawN(N,freq) : _        // Nth-order aliasing-suppressed sawtooth using DPW method (see below)
sawNp(N,freq,phase) : _ // sawN with phase offset feature
saw2dpw(freq) : _       // saw2 using DPW
saw2ptr(freq) : _       // saw2 using the faster, stateless PTR method
saw2(freq) : _          // DPW method, but subject to change if a better method emerges
saw3(freq) : _          // sawN(3)
saw4(freq) : _          // sawN(4)
sawtooth(freq) : _      // saw2
saw2f2(freq) : _        // saw2dpw with 2nd-order droop-correction filtering
saw2f4(freq) : _        // saw2dpw with 4th-order droop-correction filtering
```
Where:
* `N`: polynomial order, a constant numerical expression between 1 and 4
* `freq`: frequency in Hz
* `phase`: phase between 0 and 1
#### Test
```faust
os = library("oscillators.lib");
sawN_test = os.sawN(3, 440);
```
#### Method
Differentiated Polynomial Wave (DPW).
##### Reference
"Alias-Suppressed Oscillators based on Differentiated Polynomial Waveforms",
Vesa Valimaki, Juhan Nam, Julius Smith, and Jonathan Abel,
IEEE Tr. Audio, Speech, and Language Processing (IEEE-ASLP),
Vol. 18, no. 5, pp 786-798, May 2010.
10.1109/TASL.2009.2026507.
#### Notes
The polynomial order `N` is limited to 4 because noise has been
observed at very low `freq` values.  (LFO sawtooths should of course
be generated using `lf_sawpos` instead.)
--- sawN for N = 1 to 4 ---
Orders 5 and 6 have noise at low fundamentals: MAX_SAW_ORDER = 6; MAX_SAW_ORDER_NEXTPOW2 = 8;

---

## os.sawNp

------------------`(os.)sawNp`--------------------------------
Same as `(os.)sawN` but with a controllable waveform phase.
#### Usage
```faust
sawNp(N,freq,phase) : _
```
where
* `N`: waveform interpolation polynomial order 1 to 4 (constant integer expression)
* `freq`: frequency in Hz
* `phase`: waveform phase as a fraction of one period (rounded to nearest sample)
#### Test
```faust
os = library("oscillators.lib");
sawNp_test = os.sawNp(3, 330, 0.5);
```
#### Implementation Notes
The phase offset is implemented by delaying `sawN(N,freq)` by
`round(phase*ma.SR/freq)` samples, for up to 8191 samples.
The minimum sawtooth frequency that can be delayed a whole period
is therefore `ma.SR/8191`, which is well below audibility for normal
audio sampling rates.
--- sawNp for N = 1 to 4 ---
Phase offset = delay (max 8191 samples is more than one period of audio):

---

## os.saw2ptr

---------------------------`(os.)saw2ptr`---------------------------
Alias-Suppressed Sawtooth Audio-Frequency Oscillator
using Polynomial Transition Regions (PTR) for order 2.
#### Usage
```faust
saw2ptr(freq) : _
```
where
* `freq`: frequency in Hz
#### Test
```faust
os = library("oscillators.lib");
saw2ptr_test = os.saw2ptr(220);
```
##### Implementation
Polynomial Transition Regions (PTR) method for aliasing suppression.
##### Notes
Method PTR may be preferred because it requires less
computation and is stateless which means that the frequency `freq`
can be modulated arbitrarily fast over time without filtering
artifacts.  For this reason, `saw2` is presently defined as `saw2ptr`.
#### References
* Kleimola, J.; Valimaki, V., "Reducing Aliasing from Synthetic Audio Signals Using Polynomial Transition Regions," Signal Processing Letters, IEEE, vol.19, no.2, pp.67-70, Feb. 2012
* <https://aaltodoc.aalto.fi/bitstream/handle/123456789/7747/publication6.pdf?sequence=9>
* <http://research.spa.aalto.fi/publications/papers/spl-ptr/>
specialized reimplementation:

---

## os.saw2dpw

----------------------`(os.)saw2dpw`---------------------
Alias-Suppressed Sawtooth Audio-Frequency Oscillator
using the Differentiated Polynomial Waveform (DWP) method.
#### Usage
```faust
saw2dpw(freq) : _
```
where
* `freq`: frequency in Hz
This is the original Faust `saw2` function using the DPW method.
Since `saw2` is now defined as `saw2ptr`, the DPW version
is now available as `saw2dwp`.
#### Test
```faust
os = library("oscillators.lib");
saw2dpw_test = os.saw2dpw(220);
```

---

## os.sawtooth

------------------`(os.)sawtooth`--------------------------------
Alias-suppressed aliasing-suppressed sawtooth oscillator, presently defined as `saw2`.
`sawtooth` is a standard Faust function.
#### Usage
```faust
sawtooth(freq) : _
```
with
* `freq`: frequency in Hz
#### Test
```faust
os = library("oscillators.lib");
sawtooth_test = os.sawtooth(220);
```

---

## os.impulse

------------------`(os.)impulse`--------------------------------
One-time impulse generated when the Faust process is started.
`impulse` is a standard Faust function.
#### Usage
```faust
impulse : _
```
#### Test
```faust
os = library("oscillators.lib");
impulse_test = os.impulse;
```

---

## os.pulsetrainN

------------------`(os.)pulsetrainN`--------------------------------
Alias-suppressed pulse train oscillator.
#### Usage
```faust
pulsetrainN(N,freq,duty) : _
```
Where:
* `N`: order, as a constant numerical expression
* `freq`: frequency in Hz
* `duty`: duty cycle between 0 and 1
#### Test
```faust
os = library("oscillators.lib");
pulsetrainN_test = os.pulsetrainN(3, 220, 0.25);
```

---

## os.pulsetrain

------------------`(os.)pulsetrain`--------------------------------
Alias-suppressed pulse train oscillator. Based on `pulsetrainN(2)`.
`pulsetrain` is a standard Faust function.
#### Usage
```faust
pulsetrain(freq,duty) : _
```
Where:
* `freq`: frequency in Hz
* `duty`: duty cycle between 0 and 1
#### Test
```faust
os = library("oscillators.lib");
pulsetrain_test = os.pulsetrain(220, 0.25);
```

---

## os.squareN

------------------`(os.)squareN`--------------------------------
Alias-suppressed square wave oscillator.
#### Usage
```faust
squareN(N,freq) : _
```
Where:
* `N`: order, as a constant numerical expression
* `freq`: frequency in Hz
#### Test
```faust
os = library("oscillators.lib");
squareN_test = os.squareN(3, 220);
```

---

## os.square

------------------`(os.)square`--------------------------------
Alias-suppressed square wave oscillator. Based on `squareN(2)`.
`square` is a standard Faust function.
#### Usage
```faust
square(freq) : _
```
Where:
* `freq`: frequency in Hz
#### Test
```faust
os = library("oscillators.lib");
square_test = os.square(220);
```

---

## os.imptrainN

------------------`(os.)imptrainN`--------------------------------
Alias-suppressed impulse train generator.
#### Usage
```faust
imptrainN(N,freq) : _
```
Where:
* `N`: order, as a constant numerical expression
* `freq`: frequency in Hz
#### Test
```faust
os = library("oscillators.lib");
imptrainN_test = os.imptrainN(4, 220);
```

---

## os.imptrain

------------------`(os.)imptrain`--------------------------------
Alias-suppressed impulse train generator. Based on `imptrainN(2)`.
`imptrain` is a standard Faust function.
#### Usage
```faust
imptrain(freq) : _
```
Where:
* `freq`: frequency in Hz
#### Test
```faust
os = library("oscillators.lib");
imptrain_test = os.imptrain(220);
```

---

## os.triangleN

------------------`(os.)triangleN`--------------------------------
Alias-suppressed triangle wave oscillator.
#### Usage
```faust
triangleN(N,freq) : _
```
Where:
* `N`: order, as a constant numerical expression
* `freq`: frequency in Hz
#### Test
```faust
os = library("oscillators.lib");
triangleN_test = os.triangleN(3, 220);
```

---

## os.triangle

------------------`(os.)triangle`--------------------------------
Alias-suppressed triangle wave oscillator. Based on `triangleN(2)`.
`triangle` is a standard Faust function.
#### Usage
```faust
triangle(freq) : _
```
Where:
* `freq`: frequency in Hz
#### Test
```faust
os = library("oscillators.lib");
triangle_test = os.triangle(220);
```

---

## os.oscb

--------------------------`(os.)oscb`--------------------------------
Sinusoidal oscillator based on the biquad.
#### Usage
```faust
oscb(freq) : _
```
Where:
* `freq`: frequency in Hz
#### Test
```faust
os = library("oscillators.lib");
oscb_test = os.oscb(440);
oscrq_test = os.oscrq(440);
oscrs_test = os.oscrs(440);
oscrc_test = os.oscrc(440);
oscs_test = os.oscs(440);
```

---

## os.oscrq

--------------------------`(os.)oscrq`---------------------------
Sinusoidal (sine and cosine) oscillator based on 2D vector rotation,
= undamped "coupled-form" resonator
= lossless 2nd-order normalized ladder filter.
#### Usage
```faust
oscrq(freq) : _,_
```
Where:
* `freq`: frequency in Hz
#### Test
```faust
os = library("oscillators.lib");
oscrq_test = os.oscrq(440);
```
#### References
* <https://ccrma.stanford.edu/~jos/pasp/Normalized_Scattering_Junctions.html>

---

## os.oscrs

--------------------------`(os.)oscrs`---------------------------
Sinusoidal (sine) oscillator based on 2D vector rotation,
= undamped "coupled-form" resonator
= lossless 2nd-order normalized ladder filter.
#### Usage
```faust
oscrs(freq) : _
```
Where:
* `freq`: frequency in Hz
#### Test
```faust
os = library("oscillators.lib");
oscrs_test = os.oscrs(440);
```
#### References
* <https://ccrma.stanford.edu/~jos/pasp/Normalized_Scattering_Junctions.html>

---

## os.oscrc

--------------------------`(os.)oscrc`---------------------------
Sinusoidal (cosine) oscillator based on 2D vector rotation,
= undamped "coupled-form" resonator
= lossless 2nd-order normalized ladder filter.
#### Usage
```faust
oscrc(freq) : _
```
Where:
* `freq`: frequency in Hz
#### Test
```faust
os = library("oscillators.lib");
oscrc_test = os.oscrc(440);
```
#### References
* <https://ccrma.stanford.edu/~jos/pasp/Normalized_Scattering_Junctions.html>

---

## os.oscs

--------------------------`(os.)oscs`--------------------------------
Sinusoidal oscillator based on the state variable filter
= undamped "modified-coupled-form" resonator
= "magic circle" algorithm used in graphics.
#### Usage
```faust
oscs(freq) : _
```
Where:
* `freq`: frequency in Hz
#### Test
```faust
os = library("oscillators.lib");
oscs_test = os.oscs(440);
```

---

## os.quadosc

-----------------`(os.)quadosc`--------------------
Quadrature (cosine and sine) oscillator based on QuadOsc by Martin Vicanek.
#### Usage
```faust
quadosc(freq) : _,_
```
where
* `freq`: frequency in Hz
#### Test
```faust
os = library("oscillators.lib");
quadosc_test = os.quadosc(440);
```
#### References
* <https://vicanek.de/articles/QuadOsc.pdf>
Authors:
Dario Sanfilippo <sanfilippo.dario@gmail.com>
and Oleg Nesterov (JOS ed.)

---

## os.sidebands

-----------------------------`(os.)sidebands`--------------------------------------
Adds harmonics to quad oscillator.
#### Usage
```faust
cos(x),sin(x) : sidebands(vs) : _,_
```
Where:
* `vs` : list of amplitudes
#### Test
```faust
os = library("oscillators.lib");
sidebands_test = os.quadosc(110) : os.sidebands((1, 0.5, 0.25));
```
#### Example test program
```faust
cos(x),sin(x) : sidebands((10,20,30))
```
outputs:
```faust
10*cos(x) + 20*cos(2*x) + 30*cos(3*x),
10*sin(x) + 20*sin(2*x) + 30*sin(3*x);
```
The following:
```faust
process = os.quadosc(F) : sidebands((10,20,30))
```
is (modulo floating point issues) the same as:
```faust
c = os.quadosc : _,!;
s = os.quadosc : !,_;
process =
10*c(F) + 20*c(2*F) + 30*c(F),
10*s(F) + 20*s(2*F) + 30*s(F);
```
but much more efficient.
#### Implementation Notes
This is based on the trivial trigonometric identities:
```faust
cos((n + 1) x) = 2 cos(x) cos(n x) - cos((n - 1) x)
sin((n + 1) x) = 2 cos(x) sin(n x) - sin((n - 1) x)
```
Note that the calculation of the cosine/sine parts do not depend
on each other, so if you only need the sine part you can do:
```faust
process = os.quadosc(F) : sidebands(vs) : !,_;
```
and the compiler will discard the half of the calculations.

---

## os.sidebands_list

-----------------------------`(os.)sidebands_list`--------------------------------------
Creates the list of complex harmonics from quad oscillator.
Similar to `sidebands` but doesn't sum the harmonics, so it is more
generic but less convenient for immediate usage.
#### Usage
```faust
cos(x),sin(x) : sidebands_list(N) : si.bus(2*N)
```
Where:
* `N` : number of harmonics, compile time constant > 1
#### Test
```faust
os = library("oscillators.lib");
sidebands_list_test = os.quadosc(110) : os.sidebands_list(3);
```
#### Example test program
```faust
cos(x),sin(x) : sidebands_list(3)
```
outputs:
```faust
cos(x),sin(x), cos(2*x),sin(2*x), cos(3*x),sin(3*x);
```
The following:
```faust
process = os.quadosc(F) : sidebands_list(3)
```
is (modulo floating point issues) the same as:
```faust
process = os.quadosc(F), os.quadosc(2*F), os.quadosc(3*F);
```
but much more efficient.

---

## os.dsf

------------------------------`(os.)dsf`--------------------------------
An environment with sine/cosine oscsillators with exponentially decaying
harmonics based on direct summation formula.
#### Usage
```faust
dsf.xxx(f0, df, a, [n]) : _
```
Where:
* `f0`: base frequency
* `df`: step frequency
* `a`: decaying factor != 1
* `n`: total number of harmonics (`osccN/oscsN` only)
#### Test
```faust
os = library("oscillators.lib");
dsf_oscc_test = os.dsf.oscc(220, 110, 0.6);
dsf_oscs_test = os.dsf.oscs(220, 110, 0.6);
dsf_osccN_test = os.dsf.osccN(220, 110, 0.6, 4);
dsf_oscsN_test = os.dsf.oscsN(220, 110, 0.6, 4);
dsf_osccNq_test = os.dsf.osccNq(220, 110, 0.6);
dsf_oscsNq_test = os.dsf.oscsNq(220, 110, 0.6);
```
#### Variants
- infinite number of harmonics, implies aliasing
```faust
oscc(f0,df,a) : _;
oscs(f0,df,a) : _;
```
- n harmonics, f0, f0 + df, f0 + 2\*df, ..., f0 + (n-1)\*df
```faust
osccN(f0,df,a,n) : _;
oscsN(f0,df,a,n) : _;
```
- finite number of harmonics, from f0 to Nyquist
```faust
osccNq(f0,df,a) : _;
oscsNq(f0,df,a) : _;
```
#### Example test program
```faust
process = dsf.osccN(F0,DF,A,N),
dsf.oscsN(F0,DF,A,N);
```
if `N` is an integer constant, the same (modulo fp issues) as:
```faust
c = os.quadosc : _,!;
s = os.quadosc : !,_;
process = sum(k,N, A^k * c(F0 + k*DF)),
sum(k,N, A^k * s(F0 + k*DF));
```
but much more efficient.
#### References
* <https://ccrma.stanford.edu/STANM/stanms/stanm5/stanm5.pdf>

---

## os.oscwc

-----------------`(os.)oscwc`--------------------
Sinusoidal oscillator based on the waveguide resonator `wgr`. Unit-amplitude
cosine oscillator.
#### Usage
```faust
oscwc(freq) : _
```
Where:
* `freq`: frequency in Hz
#### Test
```faust
os = library("oscillators.lib");
oscwc_test = os.oscwc(440);
```
#### References
* <https://ccrma.stanford.edu/~jos/pasp/Digital_Waveguide_Oscillator.html>

---

## os.oscws

-----------------`(os.)oscws`--------------------
Sinusoidal oscillator based on the waveguide resonator `wgr`. Unit-amplitude
sine oscillator.
#### Usage
```faust
oscws(freq) : _
```
Where:
* `freq`: frequency in Hz
#### Test
```faust
os = library("oscillators.lib");
oscws_test = os.oscws(440);
```
#### References
* <https://ccrma.stanford.edu/~jos/pasp/Digital_Waveguide_Oscillator.html>

---

## os.oscq

-----------------`(os.)oscq`--------------------
Sinusoidal oscillator based on the waveguide resonator `wgr`.
Unit-amplitude cosine and sine (quadrature) oscillator.
#### Usage
```faust
oscq(freq) : _,_
```
Where:
* `freq`: frequency in Hz
#### Test
```faust
os = library("oscillators.lib");
oscq_test = os.oscq(440);
```
#### References
* <https://ccrma.stanford.edu/~jos/pasp/Digital_Waveguide_Oscillator.html>

---

## os.oscw

-----------------`(os.)oscw`--------------------
Sinusoidal oscillator based on the waveguide resonator `wgr`.
Unit-amplitude cosine oscillator (default).
#### Usage
```faust
oscw(freq) : _
```
Where:
* `freq`: frequency in Hz
#### Test
```faust
os = library("oscillators.lib");
oscw_test = os.oscw(440);
```
#### References
* <https://ccrma.stanford.edu/~jos/pasp/Digital_Waveguide_Oscillator.html>

---

## os.CZsaw

----------`(os.)CZsaw`----------
Oscillator that mimics the Casio CZ saw oscillator.
`CZsaw` is a standard Faust function.
#### Usage
```faust
CZsaw(fund,index) : _
```
Where:
* `fund`: a saw-tooth waveform between 0 and 1 that the oscillator slaves to
* `index`: the brightness of the oscillator, 0 to 1. 0 = sine-wave, 1 = saw-wave
#### Test
```faust
os = library("oscillators.lib");
CZsaw_test = os.CZsaw(os.lf_sawpos(110), 0.5);
```
CZ oscillators by Mike Moser-Booth:
<https://forum.pdpatchrepo.info/topic/5992/casio-cz-oscillators>
Ported from pd to Faust by Bart Brouns

---

## os.CZsawP

----------`(os.)CZsawP`----------
Oscillator that mimics the Casio CZ saw oscillator,
with it's phase aligned to `fund:sin`.
`CZsawP` is a standard Faust function.
#### Usage
```faust
CZsawP(fund,index) : _
```
Where:
* `fund`: a saw-tooth waveform between 0 and 1 that the oscillator slaves to
* `index`: the brightness of the oscillator, 0 to 1. 0 = sine-wave, 1 = saw-wave
#### Test
```faust
os = library("oscillators.lib");
CZsawP_test = os.CZsawP(os.lf_sawpos(110), 0.5);
```
CZ oscillators by Mike Moser-Booth:
<https://forum.pdpatchrepo.info/topic/5992/casio-cz-oscillators>
Ported from pd to Faust by Bart Brouns

---

## os.CZsquare

----------`(os.)CZsquare`----------
Oscillator that mimics the Casio CZ square oscillator
`CZsquare` is a standard Faust function.
#### Usage
```faust
CZsquare(fund,index) : _
```
Where:
* `fund`: a saw-tooth waveform between 0 and 1 that the oscillator slaves to
* `index`: the brightness of the oscillator, 0 to 1. 0 = sine-wave, 1 = square-wave
#### Test
```faust
os = library("oscillators.lib");
CZsquare_test = os.CZsquare(os.lf_sawpos(110), 0.5);
```
CZ oscillators by Mike Moser-Booth:
<https://forum.pdpatchrepo.info/topic/5992/casio-cz-oscillators>
Ported from pd to Faust by Bart Brouns

---

## os.CZsquareP

----------`(os.)CZsquareP`----------
Oscillator that mimics the Casio CZ square oscillator,
with it's phase aligned to `fund:sin`.
`CZsquareP` is a standard Faust function.
#### Usage
```faust
CZsquareP(fund,index) : _
```
Where:
* `fund`: a saw-tooth waveform between 0 and 1 that the oscillator slaves to
* `index`: the brightness of the oscillator, 0 to 1. 0 = sine-wave, 1 = square-wave
#### Test
```faust
os = library("oscillators.lib");
CZsquareP_test = os.CZsquareP(os.lf_sawpos(110), 0.5);
```
CZ oscillators by Mike Moser-Booth:
<https://forum.pdpatchrepo.info/topic/5992/casio-cz-oscillators>
Ported from pd to Faust by Bart Brouns

---

## os.CZpulse

----------`(os.)CZpulse`----------
Oscillator that mimics the Casio CZ pulse oscillator.
`CZpulse` is a standard Faust function.
#### Usage
```faust
CZpulse(fund,index) : _
```
Where:
* `fund`: a saw-tooth waveform between 0 and 1 that the oscillator slaves to
* `index`: the brightness of the oscillator, 0 gives a sine-wave, 1 is closer to a pulse
#### Test
```faust
os = library("oscillators.lib");
CZpulse_test = os.CZpulse(os.lf_sawpos(110), 0.5);
```
CZ oscillators by Mike Moser-Booth:
<https://forum.pdpatchrepo.info/topic/5992/casio-cz-oscillators>
Ported from pd to Faust by Bart Brouns

---

## os.CZpulseP

----------`(os.)CZpulseP`----------
Oscillator that mimics the Casio CZ pulse oscillator,
with it's phase aligned to `fund:sin`.
`CZpulseP` is a standard Faust function.
#### Usage
```faust
CZpulseP(fund,index) : _
```
Where:
* `fund`: a saw-tooth waveform between 0 and 1 that the oscillator slaves to
* `index`: the brightness of the oscillator, 0 gives a sine-wave, 1 is closer to a pulse
#### Test
```faust
os = library("oscillators.lib");
CZpulseP_test = os.CZpulseP(os.lf_sawpos(110), 0.5);
```
CZ oscillators by Mike Moser-Booth:
<https://forum.pdpatchrepo.info/topic/5992/casio-cz-oscillators>
Ported from pd to Faust by Bart Brouns

---

## os.CZsinePulse

----------`(os.)CZsinePulse`----------
Oscillator that mimics the Casio CZ sine/pulse oscillator.
`CZsinePulse` is a standard Faust function.
#### Usage
```faust
CZsinePulse(fund,index) : _
```
Where:
* `fund`: a saw-tooth waveform between 0 and 1 that the oscillator slaves to
* `index`: the brightness of the oscillator, 0 gives a sine-wave, 1 is a sine minus a pulse
#### Test
```faust
os = library("oscillators.lib");
CZsinePulse_test = os.CZsinePulse(os.lf_sawpos(110), 0.5);
```
CZ oscillators by Mike Moser-Booth:
<https://forum.pdpatchrepo.info/topic/5992/casio-cz-oscillators>
Ported from pd to Faust by Bart Brouns

---

## os.CZsinePulseP

----------`(os.)CZsinePulseP`----------
Oscillator that mimics the Casio CZ sine/pulse oscillator,
with it's phase aligned to `fund:sin`.
`CZsinePulseP` is a standard Faust function.
#### Usage
```faust
CZsinePulseP(fund,index) : _
```
Where:
* `fund`: a saw-tooth waveform between 0 and 1 that the oscillator slaves to
* `index`: the brightness of the oscillator, 0 gives a sine-wave, 1 is a sine minus a pulse
#### Test
```faust
os = library("oscillators.lib");
CZsinePulseP_test = os.CZsinePulseP(os.lf_sawpos(110), 0.5);
```
CZ oscillators by Mike Moser-Booth:
<https://forum.pdpatchrepo.info/topic/5992/casio-cz-oscillators>
Ported from pd to Faust by Bart Brouns

---

## os.CZhalfSine

----------`(os.)CZhalfSine`----------
Oscillator that mimics the Casio CZ half sine oscillator.
`CZhalfSine` is a standard Faust function.
#### Usage
```faust
CZhalfSine(fund,index) : _
```
Where:
* `fund`: a saw-tooth waveform between 0 and 1 that the oscillator slaves to
* `index`: the brightness of the oscillator, 0 gives a sine-wave, 1 is somewhere between a saw and a square
#### Test
```faust
os = library("oscillators.lib");
CZhalfSine_test = os.CZhalfSine(os.lf_sawpos(110), 0.5);
```
CZ oscillators by Mike Moser-Booth:
<https://forum.pdpatchrepo.info/topic/5992/casio-cz-oscillators>
Ported from pd to Faust by Bart Brouns

---

## os.CZhalfSineP

----------`(os.)CZhalfSineP`----------
Oscillator that mimics the Casio CZ half sine oscillator,
with it's phase aligned to `fund:sin`.
`CZhalfSineP` is a standard Faust function.
#### Usage
```faust
CZhalfSineP(fund,index) : _
```
Where:
* `fund`: a saw-tooth waveform between 0 and 1 that the oscillator slaves to
* `index`: the brightness of the oscillator, 0 gives a sine-wave, 1 is somewhere between a saw and a square
#### Test
```faust
os = library("oscillators.lib");
CZhalfSineP_test = os.CZhalfSineP(os.lf_sawpos(110), 0.5);
```
CZ oscillators by Mike Moser-Booth:
<https://forum.pdpatchrepo.info/topic/5992/casio-cz-oscillators>
Ported from pd to Faust by Bart Brouns

---

## os.CZresSaw

----------`(os.)CZresSaw`----------
Oscillator that mimics the Casio CZ resonant sawtooth oscillator.
`CZresSaw` is a standard Faust function.
#### Usage
```faust
CZresSaw(fund,res) : _
```
Where:
* `fund`: a saw-tooth waveform between 0 and 1 that the oscillator slaves to
* `res`: the frequency of resonance as a factor of the fundamental pitch.
#### Test
```faust
os = library("oscillators.lib");
CZresSaw_test = os.CZresSaw(os.lf_sawpos(110), 2.5);
```
CZ oscillators by Mike Moser-Booth:
<https://forum.pdpatchrepo.info/topic/5992/casio-cz-oscillators>
Ported from pd to Faust by Bart Brouns

---

## os.CZresTriangle

----------`(os.)CZresTriangle`----------
Oscillator that mimics the Casio CZ resonant triangle oscillator.
`CZresTriangle` is a standard Faust function.
#### Usage
```faust
CZresTriangle(fund,res) : _
```
Where:
* `fund`: a saw-tooth waveform between 0 and 1 that the oscillator slaves to
* `res`: the frequency of resonance as a factor of the fundamental pitch.
#### Test
```faust
os = library("oscillators.lib");
CZresTriangle_test = os.CZresTriangle(os.lf_sawpos(110), 2.5);
```
CZ oscillators by Mike Moser-Booth:
<https://forum.pdpatchrepo.info/topic/5992/casio-cz-oscillators>
Ported from pd to Faust by Bart Brouns

---

## os.CZresTrap

----------`(os.)CZresTrap`----------
Oscillator that mimics the Casio CZ resonant trapeze oscillator
`CZresTrap` is a standard Faust function.
#### Usage
```faust
CZresTrap(fund,res) : _
```
Where:
* `fund`: a saw-tooth waveform between 0 and 1 that the oscillator slaves to
* `res`: the frequency of resonance as a factor of the fundamental pitch.
#### Test
```faust
os = library("oscillators.lib");
CZresTrap_test = os.CZresTrap(os.lf_sawpos(110), 2.5);
```
CZ oscillators by Mike Moser-Booth:
<https://forum.pdpatchrepo.info/topic/5992/casio-cz-oscillators>
Ported from pd to Faust by Bart Brouns

---

## os.polyblep

----------`(os.)polyblep`----------
PolyBLEP residual function, used for smoothing steps in the audio signal.
#### Usage
```faust
polyblep(Q,phase) : _
```
Where:
* `Q`: smoothing factor between 0 and 0.5. Determines how far from the ends of the phase interval the quadratic function is used.
* `phase`: normalised phase (between 0 and 1)
#### Test
```faust
os = library("oscillators.lib");
polyblep_test = os.polyblep(0.2, os.lf_sawpos(220));
```

---

## os.polyblep_saw

----------`(os.)polyblep_saw`----------
Sawtooth oscillator with suppressed aliasing (using `polyblep`).
#### Usage
```faust
polyblep_saw(freq) : _
```
Where:
* `freq`: frequency in Hz
#### Test
```faust
os = library("oscillators.lib");
polyblep_saw_test = os.polyblep_saw(220);
```

---

## os.polyblep_square

----------`(os.)polyblep_square`----------
Square wave oscillator with suppressed aliasing (using `polyblep`).
#### Usage
```faust
polyblep_square(freq) : _
```
Where:
* `freq`: frequency in Hz
#### Test
```faust
os = library("oscillators.lib");
polyblep_square_test = os.polyblep_square(220);
```

---

## os.polyblep_triangle

----------`(os.)polyblep_triangle`----------
Triangle wave oscillator with suppressed aliasing (using `polyblep`).
#### Usage
```faust
polyblep_triangle(freq) : _
```
Where:
* `freq`: frequency in Hz
#### Test
```faust
os = library("oscillators.lib");
polyblep_triangle_test = os.polyblep_triangle(220);
```

---

# phaflangers.lib
**Prefix:** `pf`

################################ phaflangers.lib ##########################################
Phasers and Flangers library. Its official prefix is `pf`.

This library provides a set of phaser and flanger effects based on delay-line
modulation.

The Phaflangers library is organized into 1 section:

* [Functions Reference](#functions-reference)

#### References

* <https://github.com/grame-cncm/faustlibraries/blob/master/phaflangers.lib>
########################################################################################

## pf.flanger_mono

---------------`(pf.)flanger_mono`-------------
Mono flanging effect.
#### Usage:
```faust
_ : flanger_mono(dmax,curdel,depth,fb,invert) : _
```
Where:
* `dmax`: maximum delay-line length (power of 2) - 10 ms typical
* `curdel`: current dynamic delay (not to exceed dmax)
* `depth`: effect strength between 0 and 1 (1 typical)
* `fb`: feedback gain between 0 and 1 (0 typical)
* `invert`: 0 for normal, 1 to invert sign of flanging sum
#### Test
```faust
pf = library("phaflangers.lib");
os = library("oscillators.lib");
flanger_mono_test = os.osc(440) : pf.flanger_mono(4096, 1024, 0.7, 0.25, 0);
```
#### References
* <https://ccrma.stanford.edu/~jos/pasp/Flanging.html>

---

## pf.flanger_stereo

---------------`(pf.)flanger_stereo`-------------
Stereo flanging effect.
`flanger_stereo` is a standard Faust function.
#### Usage:
```faust
_,_ : flanger_stereo(dmax,curdel1,curdel2,depth,fb,invert) : _,_
```
Where:
* `dmax`: maximum delay-line length (power of 2) - 10 ms typical
* `curdel1`: current dynamic delay for the left channel (not to exceed dmax)
* `curdel2`: current dynamic delay for the right channel (not to exceed dmax)
* `depth`: effect strength between 0 and 1 (1 typical)
* `fb`: feedback gain between 0 and 1 (0 typical)
* `invert`: 0 for normal, 1 to invert sign of flanging sum
#### Test
```faust
pf = library("phaflangers.lib");
os = library("oscillators.lib");
flanger_stereo_test = os.osc(440), os.osc(660) : pf.flanger_stereo(4096, 1024, 1536, 0.7, 0.25, 0);
```
#### References
* <https://ccrma.stanford.edu/~jos/pasp/Flanging.html>

---

## pf.phaser2_mono

-------`(pf.)phaser2_mono`-----------------
Mono phasing effect.
#### Phaser
```faust
_ : phaser2_mono(Notches,phase,width,frqmin,fratio,frqmax,speed,depth,fb,invert) : _
```
Where:
* `Notches`: number of spectral notches (MACRO ARGUMENT - not a signal)
* `phase`: phase of the oscillator (0-1)
* `width`: approximate width of spectral notches in Hz
* `frqmin`: approximate minimum frequency of first spectral notch in Hz
* `fratio`: ratio of adjacent notch frequencies
* `frqmax`: approximate maximum frequency of first spectral notch in Hz
* `speed`: LFO frequency in Hz (rate of periodic notch sweep cycles)
* `depth`: effect strength between 0 and 1 (1 typical) (aka "intensity")
when depth=2, "vibrato mode" is obtained (pure allpass chain)
* `fb`: feedback gain between -1 and 1 (0 typical)
* `invert`: 0 for normal, 1 to invert sign of flanging sum
#### Test
```faust
pf = library("phaflangers.lib");
os = library("oscillators.lib");
phaser2_mono_test = os.osc(330) : pf.phaser2_mono(4, 0.0, 50, 200, 1.5, 4000, 0.5, 0.8, 0.2, 0);
```
#### References
* <https://ccrma.stanford.edu/~jos/pasp/Phasing.html>
* <http://www.geofex.com/Article_Folders/phasers/phase.html>
* 'An Allpass Approach to Digital Phasing and Flanging', Julius O. Smith III,
Proc. Int. Computer Music Conf. (ICMC-84), pp. 103-109, Paris, 1984.
* CCRMA Tech. Report STAN-M-21: <https://ccrma.stanford.edu/STANM/stanms/stanm21/>

---

## pf.phaser2_stereo

-------`(pf.)phaser2_stereo`-------
Stereo phasing effect.
`phaser2_stereo` is a standard Faust function.
#### Phaser
```faust
_,_ : phaser2_stereo(Notches,width,frqmin,fratio,frqmax,speed,depth,fb,invert) : _,_
```
Where:
* `Notches`: number of spectral notches (MACRO ARGUMENT - not a signal)
* `width`: approximate width of spectral notches in Hz
* `frqmin`: approximate minimum frequency of first spectral notch in Hz
* `fratio`: ratio of adjacent notch frequencies
* `frqmax`: approximate maximum frequency of first spectral notch in Hz
* `speed`: LFO frequency in Hz (rate of periodic notch sweep cycles)
* `depth`: effect strength between 0 and 1 (1 typical) (aka "intensity")
when depth=2, "vibrato mode" is obtained (pure allpass chain)
* `fb`: feedback gain between -1 and 1 (0 typical)
* `invert`: 0 for normal, 1 to invert sign of flanging sum
#### Test
```faust
pf = library("phaflangers.lib");
os = library("oscillators.lib");
phaser2_stereo_test = os.osc(220), os.osc(330) : pf.phaser2_stereo(4, 50, 200, 1.5, 4000, 0.5, 0.8, 0.2, 0);
```
#### References
* <https://ccrma.stanford.edu/~jos/pasp/Phasing.html>
* <http://www.geofex.com/Article_Folders/phasers/phase.html>
* 'An Allpass Approach to Digital Phasing and Flanging', Julius O. Smith III,
Proc. Int. Computer Music Conf. (ICMC-84), pp. 103-109, Paris, 1984.
* CCRMA Tech. Report STAN-M-21: <https://ccrma.stanford.edu/STANM/stanms/stanm21/>

---

# physmodels.lib
**Prefix:** `pm`

##################################### physmodels.lib ###################################
Faust physical modeling library. Its official prefix is `pm`.

This library provides an environment to facilitate physical modeling of musical
instruments. It includes waveguide, mass-spring, and digital wave
models for strings, membranes, bars, and resonant systems used in physical modeling
synthesis and acoustic simulation research. It contains dozens of functions implementing
low and high level elements going from a simple waveguide to fully operational models with
built-in UI, etc.

It is organized as follows:

* [Global Variables](#global-variables): useful pre-defined variables for
physical modeling (e.g., speed of sound, etc.).
* [Conversion Tools](#conversion-tools-1): conversion functions specific
to physical modeling (e.g., length to frequency, etc.).
* [Bidirectional Utilities](#bidirectional-utilities): functions to create
bidirectional block diagrams for physical modeling.
* [Basic Elements](#basic-elements-1): waveguides, specific types of filters, etc.
* [String Instruments](#string-instruments): various types of strings
(e.g., steel, nylon, etc.), bridges, guitars, etc.
* [Bowed String Instruments](#bowed-string-instruments): parts and models
specific to bowed string instruments (e.g., bows, bridges, violins, etc.).
* [Wind Instrument](#wind-instruments): parts and models specific to wind
instruments (e.g., reeds, mouthpieces, flutes, clarinets, etc.).
* [Exciters](#exciters): pluck generators, "blowers", etc.
* [Modal Percussions](#modal-percussions): percussion instruments based on
modal models.
* [Vocal Synthesis](#vocal-synthesis): functions for various vocal synthesis
techniques (e.g., fof, source/filter, etc.) and vocal synthesizers.
* [Misc Functions](#misc-functions): any other functions that don't fit in
the previous category (e.g., nonlinear filters, etc.).

This library is part of the Faust Physical Modeling ToolKit.
More information on how to use this library can be found on this [page](https://ccrma.stanford.edu/~rmichon/pmFaust) or this [video](https://faust.grame.fr/community/events/#introduction-to-the-faust-physical-modeling-toolkit-romain-michon). Tutorials on how to make
physical models of musical instruments using Faust can be found
[here](https://ccrma.stanford.edu/~rmichon/faustTutorials/#making-physical-models-of-musical-instruments-with-faust) as well.

#### References

* <https://github.com/grame-cncm/faustlibraries/blob/master/physmodels.lib>
########################################################################################
Authors: Romain Michon, Pierre-Amaury Grumiaux, and Yann Orlarey

## pm.speedOfSound

--------------`(pm.)speedOfSound`----------
Speed of sound in meters per second (340m/s).

---

## pm.maxLength

--------------`(pm.)maxLength`----------
The default maximum length (3) in meters of strings and tubes used in this
library. This variable should be overriden to allow longer strings or tubes.

---

## pm.f2l

--------------`(pm.)f2l`----------
Frequency to length in meters.
#### Usage
```faust
f2l(freq) : distanceInMeters
```
Where:
* `freq`: the frequency
#### Test
```faust
pm = library("physmodels.lib");
f2l_test = pm.f2l(440);
```

---

## pm.l2f

--------------`(pm.)l2f`----------
Length in meters to frequency.
#### Usage
```faust
l2f(length) : freq
```
Where:
* `length`: length/distance in meters
#### Test
```faust
pm = library("physmodels.lib");
l2f_test = pm.l2f(0.75);
```

---

## pm.l2s

--------------`(pm.)l2s`----------
Length in meters to number of samples.
#### Usage
```faust
l2s(l) : numberOfSamples
```
Where:
* `l`: length in meters
#### Test
```faust
pm = library("physmodels.lib");
l2s_test = pm.l2s(1.2);
```

---

## pm.basicBlock

--------------`(pm.)basicBlock`----------
Empty bidirectional block to be used with [`chain`](#chain): 3 signals ins
and 3 signals out.
#### Usage
```faust
chain(basicBlock : basicBlock : etc.)
```
#### Test
```faust
pm = library("physmodels.lib");
basicBlock_test = 0,0,0 : pm.basicBlock;
```

---

## pm.chain

-------`(pm.)chain`----------
Creates a chain of bidirectional blocks.
Blocks must have 3 inputs and outputs. The first input/output carry left
going waves, the second input/output carry right going waves, and the third
input/output is used to carry any potential output signal to the end of the
algorithm. The implied one sample delay created by the `~` operator is
generalized to the left and right going waves. Thus, `n` blocks in `chain()`
will add an `n` samples delay to both left and right going waves.
#### Usage
```faust
leftGoingWaves,rightGoingWaves,mixedOutput : chain( A : B ) : leftGoingWaves,rightGoingWaves,mixedOutput
with {
A = _,_,_;
B = _,_,_;
};
```
#### Test
```faust
pm = library("physmodels.lib");
chain_test = 0,0,0 : pm.chain(pm.in(0.1) : pm.basicBlock);
```

---

## pm.inLeftWave

-------`(pm.)inLeftWave`--------------
Adds a signal to left going waves anywhere in a [`chain`](#chain) of blocks.
#### Usage
```faust
model(x) = chain(A : inLeftWave(x) : B)
```
Where `A` and `B` are bidirectional blocks and `x` is the signal added to left
going waves in that chain.
#### Test
```faust
pm = library("physmodels.lib");
inLeftWave_test = 0,0,0 : pm.inLeftWave(0.25);
```

---

## pm.inRightWave

-------`(pm.)inRightWave`--------------
Adds a signal to right going waves anywhere in a [`chain`](#chain) of blocks.
#### Usage
```faust
model(x) = chain(A : inRightWave(x) : B)
```
Where `A` and `B` are bidirectional blocks and `x` is the signal added to right
going waves in that chain.
#### Test
```faust
pm = library("physmodels.lib");
inRightWave_test = 0,0,0 : pm.inRightWave(0.25);
```

---

## pm.in

-------`(pm.)in`--------------
Adds a signal to left and right going waves anywhere in a [`chain`](#chain)
of blocks.
#### Usage
```faust
model(x) = chain(A : in(x) : B)
```
Where `A` and `B` are bidirectional blocks and `x` is the signal added to
left and right going waves in that chain.
#### Test
```faust
pm = library("physmodels.lib");
in_test = 0,0,0 : pm.in(0.25);
```

---

## pm.outLeftWave

-------`(pm.)outLeftWave`--------------
Sends the signal of left going waves to the output channel of the [`chain`](#chain).
#### Usage
```faust
chain(A : outLeftWave : B)
```
Where `A` and `B` are bidirectional blocks.
#### Test
```faust
pm = library("physmodels.lib");
outLeftWave_test = pm.outLeftWave(0.1, 0.2, 0.3);
```

---

## pm.outRightWave

-------`(pm.)outRightWave`--------------
Sends the signal of right going waves to the output channel of the [`chain`](#chain).
#### Usage
```faust
chain(A : outRightWave : B)
```
Where `A` and `B` are bidirectional blocks.
#### Test
```faust
pm = library("physmodels.lib");
outRightWave_test = pm.outRightWave(0.1, 0.2, 0.3);
```

---

## pm.out

-------`(pm.)out`--------------
Sends the signal of right and left going waves to the output channel of the
[`chain`](#chain).
#### Usage
```faust
chain(A : out : B)
```
Where `A` and `B` are bidirectional blocks.
#### Test
```faust
pm = library("physmodels.lib");
out_test = pm.out(0.1, 0.2, 0.3);
```

---

## pm.terminations

-------`(pm.)terminations`--------------
Creates terminations on both sides of a [`chain`](#chain) without closing
the inputs and outputs of the bidirectional signals chain. As for
[`chain`](#chain), this function adds a 1 sample delay to the bidirectional
signal, both ways. Of course, this function can be nested within a
[`chain`](#chain).
#### Usage
```faust
terminations(a,b,c)
with {
a = *(-1); // left termination
b = chain(D : E : F); // bidirectional chain of blocks (D, E, F, etc.)
c = *(-1); // right termination
};
```
#### Test
```faust
pm = library("physmodels.lib");
terminations_test = 0,0,0 : pm.terminations(*(-1), pm.basicBlock, *(-1));
```

---

## pm.lTermination

-------`(pm.)lTermination`----------
Creates a termination on the left side of a [`chain`](#chain) without
closing the inputs and outputs of the bidirectional signals chain. This
function adds a 1 sample delay near the termination and can be nested
within another [`chain`](#chain).
#### Usage
```faust
lTerminations(a,b)
with {
a = *(-1); // left termination
b = chain(D : E : F); // bidirectional chain of blocks (D, E, F, etc.)
};
```
#### Test
```faust
pm = library("physmodels.lib");
lTermination_test = 0,0,0 : pm.lTermination(*(-1), pm.basicBlock);
```

---

## pm.rTermination

-------`(pm.)rTermination`----------
Creates a termination on the right side of a [`chain`](#chain) without
closing the inputs and outputs of the bidirectional signals chain. This
function adds a 1 sample delay near the termination and can be nested
within another [`chain`](#chain).
#### Usage
```faust
rTerminations(b,c)
with {
b = chain(D : E : F); // bidirectional chain of blocks (D, E, F, etc.)
c = *(-1); // right termination
};
```
#### Test
```faust
pm = library("physmodels.lib");
rTermination_test = 0,0,0 : pm.rTermination(pm.basicBlock, *(-1));
```

---

## pm.closeIns

-------`(pm.)closeIns`----------
Closes the inputs of a bidirectional chain in all directions.
#### Usage
```faust
closeIns : chain(...) : _,_,_
```
#### Test
```faust
pm = library("physmodels.lib");
closeIns_test = pm.closeIns;
```

---

## pm.closeOuts

-------`(pm.)closeOuts`----------
Closes the outputs of a bidirectional chain in all directions except for the
main signal output (3d output).
#### Usage
```faust
_,_,_ : chain(...) : _
```
#### Test
```faust
pm = library("physmodels.lib");
closeOuts_test = 0,0,0 : pm.closeOuts;
```

---

## pm.endChain

-------`(pm.)endChain`----------
Closes the inputs and outputs of a bidirectional chain in all directions
except for the main signal output (3d output).
#### Usage
```faust
endChain(chain(...)) : _
```
#### Test
```faust
pm = library("physmodels.lib");
endChain_test = 0,0,0 : pm.endChain(pm.basicBlock);
```

---

## pm.waveguideN

-------`(pm.)waveguideN`----------
A series of waveguide functions based on various types of delays (see
[`fdelay[n]`](#fdelayn)).
#### List of functions
* `waveguideUd`: unit delay waveguide
* `waveguideFd`: fractional delay waveguide
* `waveguideFd2`: second order fractional delay waveguide
* `waveguideFd4`: fourth order fractional delay waveguide
#### Usage
```faust
chain(A : waveguideUd(nMax,n) : B)
```
Where:
* `nMax`: the maximum length of the delays in the waveguide
* `n`: the length of the delay lines in samples.
#### Test
```faust
pm = library("physmodels.lib");
waveguideUd_test = 0,0,0 : pm.waveguideUd(512, 32);
waveguideFd_test = 0,0,0 : pm.waveguideFd(512, 32);
waveguideFd2_test = 0,0,0 : pm.waveguideFd2(512, 32);
waveguideFd4_test = 0,0,0 : pm.waveguideFd4(512, 32);
```

---

## pm.waveguide

-------`(pm.)waveguide`----------
Standard `pm.lib` waveguide (based on [`waveguideFd4`](#waveguiden)).
#### Usage
```faust
chain(A : waveguide(nMax,n) : B)
```
Where:
* `nMax`: the maximum length of the delays in the waveguide
* `n`: the length of the delay lines in samples.
#### Test
```faust
pm = library("physmodels.lib");
waveguide_test = 0,0,0 : pm.waveguide(512, 32);
```

---

## pm.bridgeFilter

-------`(pm.)bridgeFilter`----------
Generic two zeros bridge FIR filter (as implemented in the
[STK](https://ccrma.stanford.edu/software/stk/)) that can be used to
implement the reflectance violin, guitar, etc. bridges.
#### Usage
```faust
_ : bridge(brightness,absorption) : _
```
Where:
* `brightness`: controls the damping of high frequencies (0-1)
* `absorption`: controls the absorption of the brige and thus the t60 of
the string plugged to it (0-1) (1 = 20 seconds)
#### Test
```faust
pm = library("physmodels.lib");
bridgeFilter_test = pm.bridgeFilter(0.6, 0.4, os.osc(110));
```
TODO: perhaps, the coefs of this filter should be adapted in function of SR

---

## pm.modeFilter

-------`(pm.)modeFilter`----------
Resonant bandpass filter that can be used to implement a single resonance
(mode).
#### Usage
```faust
_ : modeFilter(freq,t60,gain) : _
```
Where:
* `freq`: mode frequency
* `t60`: mode resonance duration (in seconds)
* `gain`: mode gain (0-1)
#### Test
```faust
pm = library("physmodels.lib");
modeFilter_test = pm.modeFilter(440, 1.5, 0.8);
```

---

## pm.stringSegment

-------`(pm.)stringSegment`----------
A string segment without terminations (just a simple waveguide).
#### Usage
```faust
chain(A : stringSegment(maxLength,length) : B)
```
Where:
* `maxLength`: the maximum length of the string in meters (should be static)
* `length`: the length of the string in meters
#### Test
```faust
pm = library("physmodels.lib");
stringSegment_test = 0,0,0 : pm.stringSegment(1.0, 0.5);
```

---

## pm.openString

-------`(pm.)openString`----------
A bidirectional block implementing a basic "generic" string with a
selectable excitation position. Lowpass filters are built-in and
allow to simulate the effect of dispersion on the sound and thus
to change the "stiffness" of the string.
#### Usage
```faust
chain(... : openString(length,stiffness,pluckPosition,excitation) : ...)
```
Where:
* `length`: the length of the string in meters
* `stiffness`: the stiffness of the string (0-1) (1 for max stiffness)
* `pluckPosition`: excitation position (0-1) (1 is bottom)
* `excitation`: the excitation signal
#### Test
```faust
pm = library("physmodels.lib");
openString_test = 0,0,0 : pm.openString(0.8, 0.5, 0.2, pm.impulseExcitation(button("gate")));
```

---

## pm.nylonString

-------`(pm.)nylonString`----------
A bidirectional block implementing a basic nylon string with selectable
excitation position. This element is based on [`openString`](#openstring)
and has a fix stiffness corresponding to that of a nylon string.
#### Usage
```faust
chain(... : nylonString(length,pluckPosition,excitation) : ...)
```
Where:
* `length`: the length of the string in meters
* `pluckPosition`: excitation position (0-1) (1 is bottom)
* `excitation`: the excitation signal
#### Test
```faust
pm = library("physmodels.lib");
nylonString_test = 0,0,0 : pm.nylonString(0.8, 0.3, pm.impulseExcitation(button("gate")));
```

---

## pm.steelString

-------`(pm.)steelString`----------
A bidirectional block implementing a basic steel string with selectable
excitation position. This element is based on [`openString`](#openstring)
and has a fix stiffness corresponding to that of a steel string.
#### Usage
```faust
chain(... : steelString(length,pluckPosition,excitation) : ...)
```
Where:
* `length`: the length of the string in meters
* `pluckPosition`: excitation position (0-1) (1 is bottom)
* `excitation`: the excitation signal
#### Test
```faust
pm = library("physmodels.lib");
steelString_test = 0,0,0 : pm.steelString(0.8, 0.3, pm.impulseExcitation(button("gate")));
```

---

## pm.openStringPick

-------`(pm.)openStringPick`----------
A bidirectional block implementing a "generic" string with selectable
excitation position. It also has a built-in pickup whose position is the
same as the excitation position. Thus, moving the excitation position
will also move the pickup.
#### Usage
```faust
chain(... : openStringPick(length,stiffness,pluckPosition,excitation) : ...)
```
Where:
* `length`: the length of the string in meters
* `stiffness`: the stiffness of the string (0-1) (1 for max stiffness)
* `pluckPosition`: excitation position (0-1) (1 is bottom)
* `excitation`: the excitation signal
#### Test
```faust
pm = library("physmodels.lib");
openStringPick_test = 0,0,0 : pm.openStringPick(0.8, 0.4, 0.3, pm.impulseExcitation(button("gate")));
```

---

## pm.openStringPickUp

-------`(pm.)openStringPickUp`----------
A bidirectional block implementing a "generic" string with selectable
excitation position and stiffness. It also has a built-in pickup whose
position can be independenly selected. The only constraint is that the
pickup has to be placed after the excitation position.
#### Usage
```faust
chain(... : openStringPickUp(length,stiffness,pluckPosition,excitation) : ...)
```
Where:
* `length`: the length of the string in meters
* `stiffness`: the stiffness of the string (0-1) (1 for max stiffness)
* `pluckPosition`: pluck position between the top of the string and the
pickup (0-1) (1 for same as pickup position)
* `pickupPosition`: position of the pickup on the string (0-1) (1 is bottom)
* `excitation`: the excitation signal
#### Test
```faust
pm = library("physmodels.lib");
openStringPickUp_test = 0,0,0 : pm.openStringPickUp(0.8, 0.4, 0.6, 0.7, pm.impulseExcitation(button("gate")));
```

---

## pm.openStringPickDown

-------`(pm.)openStringPickDown`----------
A bidirectional block implementing a "generic" string with selectable
excitation position and stiffness. It also has a built-in pickup whose
position can be independenly selected. The only constraint is that the
pickup has to be placed before the excitation position.
#### Usage
```faust
chain(... : openStringPickDown(length,stiffness,pluckPosition,excitation) : ...)
```
Where:
* `length`: the length of the string in meters
* `stiffness`: the stiffness of the string (0-1) (1 for max stiffness)
* `pluckPosition`: pluck position on the string (0-1) (1 is bottom)
* `pickupPosition`: position of the pickup between the top of the string
and the excitation position (0-1) (1 is excitation position)
* `excitation`: the excitation signal
#### Test
```faust
pm = library("physmodels.lib");
openStringPickDown_test = 0,0,0 : pm.openStringPickDown(0.8, 0.4, 0.6, 0.5, pm.impulseExcitation(button("gate")));
```

---

## pm.ksReflexionFilter

-------`(pm.)ksReflexionFilter`----------
The "typical" one-zero Karplus-strong feedforward reflexion filter. This
filter will be typically used in a termination (see below).
#### Usage
```faust
terminations(_,chain(...),ksReflexionFilter)
```
#### Test
```faust
pm = library("physmodels.lib");
os = library("oscillators.lib");
ksReflexionFilter_test = os.osc(220) : pm.ksReflexionFilter;
```

---

## pm.rStringRigidTermination

-------`(pm.)rStringRigidTermination`----------
Bidirectional block implementing a right rigid string termination (no damping,
just phase inversion).
#### Usage
```faust
chain(rStringRigidTermination : stringSegment : ...)
```
#### Test
```faust
pm = library("physmodels.lib");
rStringRigidTermination_test = 0,0,0 : pm.rStringRigidTermination;
```

---

## pm.lStringRigidTermination

-------`(pm.)lStringRigidTermination`----------
Bidirectional block implementing a left rigid string termination (no damping,
just phase inversion).
#### Usage
```faust
chain(... : stringSegment : lStringRigidTermination)
```
#### Test
```faust
pm = library("physmodels.lib");
lStringRigidTermination_test = 0,0,0 : pm.lStringRigidTermination;
```

---

## pm.elecGuitarBridge

-------`(pm.)elecGuitarBridge`----------
Bidirectional block implementing a simple electric guitar bridge. This
block is based on [`bridgeFilter`](#bridgeFilter). The bridge doesn't
implement transmittance since it is not meant to be connected to a
body (unlike acoustic guitar). It also partially sets the resonance
duration of the string with the nuts used on the other side.
#### Usage
```faust
chain(... : stringSegment : elecGuitarBridge)
```
#### Test
```faust
pm = library("physmodels.lib");
elecGuitarBridge_test = 0,0,0 : pm.elecGuitarBridge;
```

---

## pm.elecGuitarNuts

-------`(pm.)elecGuitarNuts`----------
Bidirectional block implementing a simple electric guitar nuts. This
block is based on [`bridgeFilter`](#bridgeFilter) and does essentially
the same thing as [`elecGuitarBridge`](#elecguitarbridge), but on the
other side of the chain. It also partially sets the resonance duration of
the string with the bridge used on the other side.
#### Usage
```faust
chain(elecGuitarNuts : stringSegment : ...)
```
#### Test
```faust
pm = library("physmodels.lib");
elecGuitarNuts_test = 0,0,0 : pm.elecGuitarNuts;
```

---

## pm.guitarBridge

-------`(pm.)guitarBridge`----------
Bidirectional block implementing a simple acoustic guitar bridge. This
bridge damps more hight frequencies than
[`elecGuitarBridge`](#elecguitarbridge) and implements a transmittance
filter. It also partially sets the resonance duration of the string with
the nuts used on the other side.
#### Usage
```faust
chain(... : stringSegment : guitarBridge)
```
#### Test
```faust
pm = library("physmodels.lib");
guitarBridge_test = 0,0,0 : pm.guitarBridge;
```

---

## pm.guitarNuts

-------`(pm.)guitarNuts`----------
Bidirectional block implementing a simple acoustic guitar nuts. This
nuts damps more hight frequencies than
[`elecGuitarNuts`](#elecguitarnuts) and implements a transmittance
filter. It also partially sets the resonance duration of the string with
the bridge used on the other side.
#### Usage
```faust
chain(guitarNuts : stringSegment : ...)
```
#### Test
```faust
pm = library("physmodels.lib");
guitarNuts_test = 0,0,0 : pm.guitarNuts;
```

---

## pm.idealString

-------`(pm.)idealString`----------
An "ideal" string with rigid terminations and where the plucking position
and the pick-up position are the same. Since terminations are rigid, this
string will ring forever.
#### Usage
```faust
1-1' : idealString(length,reflexion,xPosition,excitation)
```
With:
* `length`: the length of the string in meters
* `pluckPosition`: the plucking position (0.001-0.999)
* `excitation`: the input signal for the excitation.
#### Test
```faust
pm = library("physmodels.lib");
idealString_test = 0,0,0 : pm.idealString(0.9, 0.2, pm.impulseExcitation(button("gate")));
```

---

## pm.ks

-------`(pm.)ks`----------
A Karplus-Strong string (in that case, the string is implemented as a
one dimension waveguide).
#### Usage
```faust
ks(length,damping,excitation) : _
```
Where:
* `length`: the length of the string in meters
* `damping`: string damping (0-1)
* `excitation`: excitation signal
#### Test
```faust
pm = library("physmodels.lib");
ks_test = pm.ks(0.9, 0.3, pm.impulseExcitation(button("gate")));
```

---

## pm.ks_ui_MIDI

-------`(pm.)ks_ui_MIDI`----------
Ready-to-use, MIDI-enabled Karplus-Strong string with buil-in UI.
#### Usage
```faust
ks_ui_MIDI : _
```
#### Test
```faust
pm = library("physmodels.lib");
ks_ui_MIDI_test = pm.ks_ui_MIDI;
```

---

## pm.elecGuitarModel

-------`(pm.)elecGuitarModel`----------
A simple electric guitar model (without audio effects, of course) with
selectable pluck position.
This model implements a single string. Additional strings should be created
by making a polyphonic application out of this function. Pitch is changed by
changing the length of the string and not through a finger model.
#### Usage
```faust
elecGuitarModel(length,pluckPosition,mute,excitation) : _
```
Where:
* `length`: the length of the string in meters
* `pluckPosition`: pluck position (0-1) (1 is on the bridge)
* `mute`: mute coefficient (1 for no mute and 0 for instant mute)
* `excitation`: excitation signal
#### Test
```faust
pm = library("physmodels.lib");
elecGuitarModel_test = pm.elecGuitarModel(0.9, 0.3, 0.8, pm.impulseExcitation(button("gate")));
```

---

## pm.elecGuitar

-------`(pm.)elecGuitar`----------
A simple electric guitar model with steel strings (based on
[`elecGuitarModel`](#elecguitarmodel)) implementing an excitation
model.
This model implements a single string. Additional strings should be created
by making a polyphonic application out of this function.
#### Usage
```faust
elecGuitar(length,pluckPosition,trigger) : _
```
Where:
* `length`: the length of the string in meters
* `pluckPosition`: pluck position (0-1) (1 is on the bridge)
* `mute`: mute coefficient (1 for no mute and 0 for instant mute)
* `gain`: gain of the pluck (0-1)
* `trigger`: trigger signal (1 for on, 0 for off)
#### Test
```faust
pm = library("physmodels.lib");
elecGuitar_test = pm.elecGuitar(0.9, 0.3, 0.8, 0.6, button("gate"));
```

---

## pm.elecGuitar_ui_MIDI

-------`(pm.)elecGuitar_ui_MIDI`----------
Ready-to-use MIDI-enabled electric guitar physical model with built-in UI.
#### Usage
```faust
elecGuitar_ui_MIDI : _
```
#### Test
```faust
pm = library("physmodels.lib");
elecGuitar_ui_MIDI_test = pm.elecGuitar_ui_MIDI;
```

---

## pm.guitarBody

-------`(pm.)guitarBody`----------
WARNING: not implemented yet!
Bidirectional block implementing a simple acoustic guitar body.
#### Usage
```faust
chain(... : guitarBody)
```
#### Test
```faust
pm = library("physmodels.lib");
guitarBody_test = 0,0,0 : pm.guitarBody;
```
TODO: not implemented yet

---

## pm.guitarModel

-------`(pm.)guitarModel`----------
A simple acoustic guitar model with steel strings and selectable excitation
position. This model implements a single string. Additional strings should be created
by making a polyphonic application out of this function. Pitch is changed by
changing the length of the string and not through a finger model.
WARNING: this function doesn't currently implement a body (just strings and
bridge).
#### Usage
```faust
guitarModel(length,pluckPosition,excitation) : _
```
Where:
* `length`: the length of the string in meters
* `pluckPosition`: pluck position (0-1) (1 is on the bridge)
* `excitation`: excitation signal
#### Test
```faust
pm = library("physmodels.lib");
guitarModel_test = pm.guitarModel(0.9, 0.25, pm.impulseExcitation(button("gate")));
```

---

## pm.guitar

-------`(pm.)guitar`----------
A simple acoustic guitar model with steel strings (based on
[`guitarModel`](#guitarmodel)) implementing an excitation model.
This model implements a single string. Additional strings should be created
by making a polyphonic application out of this function.
#### Usage
```faust
guitar(length,pluckPosition,trigger) : _
```
Where:
* `length`: the length of the string in meters
* `pluckPosition`: pluck position (0-1) (1 is on the bridge)
* `gain`: gain of the excitation
* `trigger`: trigger signal (1 for on, 0 for off)
#### Test
```faust
pm = library("physmodels.lib");
guitar_test = pm.guitar(0.9, 0.25, 0.8, button("gate"));
```

---

## pm.guitar_ui_MIDI

-------`(pm.)guitar_ui_MIDI`----------
Ready-to-use MIDI-enabled steel strings acoustic guitar physical model with
built-in UI.
#### Usage
```faust
guitar_ui_MIDI : _
```
#### Test
```faust
pm = library("physmodels.lib");
guitar_ui_MIDI_test = pm.guitar_ui_MIDI;
```

---

## pm.nylonGuitarModel

-------`(pm.)nylonGuitarModel`----------
A simple acoustic guitar model with nylon strings and selectable excitation
position. This model implements a single string. Additional strings should be created
by making a polyphonic application out of this function. Pitch is changed by
changing the length of the string and not through a finger model.
WARNING: this function doesn't currently implement a body (just strings and
bridge).
#### Usage
```faust
nylonGuitarModel(length,pluckPosition,excitation) : _
```
Where:
* `length`: the length of the string in meters
* `pluckPosition`: pluck position (0-1) (1 is on the bridge)
* `excitation`: excitation signal
#### Test
```faust
pm = library("physmodels.lib");
nylonGuitarModel_test = pm.nylonGuitarModel(0.9, 0.25, pm.impulseExcitation(button("gate")));
```

---

## pm.nylonGuitar

-------`(pm.)nylonGuitar`----------
A simple acoustic guitar model with nylon strings (based on
[`nylonGuitarModel`](#nylonguitarmodel)) implementing an excitation model.
This model implements a single string. Additional strings should be created
by making a polyphonic application out of this function.
#### Usage
```faust
nylonGuitar(length,pluckPosition,trigger) : _
```
Where:
* `length`: the length of the string in meters
* `pluckPosition`: pluck position (0-1) (1 is on the bridge)
* `gain`: gain of the excitation (0-1)
* `trigger`: trigger signal (1 for on, 0 for off)
#### Test
```faust
pm = library("physmodels.lib");
nylonGuitar_test = pm.nylonGuitar(0.9, 0.25, 0.8, button("gate"));
```

---

## pm.nylonGuitar_ui_MIDI

-------`(pm.)nylonGuitar_ui_MIDI`----------
Ready-to-use MIDI-enabled nylon strings acoustic guitar physical model with
built-in UI.
#### Usage
```faust
nylonGuitar_ui_MIDI : _
```
#### Test
```faust
pm = library("physmodels.lib");
nylonGuitar_ui_MIDI_test = pm.nylonGuitar_ui_MIDI;
```

---

## pm.modeInterpRes

-------`(pm.)modeInterpRes`----------
Modular string instrument resonator based on IR measurements made on 3D
printed models. The 2D space allowing for the control of the shape and the
scale of the model is enabled by interpolating between modes parameters.
More information about this technique/project can be found here:
<https://ccrma.stanford.edu/~rmichon/3dPrintingModeling/>.
#### Usage
```faust
_ : modeInterpRes(nModes,x,y) : _
```
Where:
* `nModes`: number of modeled modes (40 max)
* `x`: shape of the resonator (0: square, 1: square with rounded corners, 2: round)
* `y`: scale of the resonator (0: small, 1: medium, 2: large)
#### Test
```faust
pm = library("physmodels.lib");
os = library("oscillators.lib");
modeInterpRes_test = os.osc(110) : pm.modeInterpRes(20, 1.0, 1.5);
```

---

## pm.modularInterpBody

-------`(pm.)modularInterpBody`----------
Bidirectional block implementing a modular string instrument resonator
(see [`modeInterpRes`](#pm.modeinterpres)).
#### Usage
```faust
chain(... : modularInterpBody(nModes,shape,scale) : ...)
```
Where:
* `nModes`: number of modeled modes (40 max)
* `shape`: shape of the resonator (0: square, 1: square with rounded corners, 2: round)
* `scale`: scale of the resonator (0: small, 1: medium, 2: large)
#### Test
```faust
pm = library("physmodels.lib");
modularInterpBody_test = 0,0,0 : pm.modularInterpBody(20, 1.0, 1.5);
```

---

## pm.modularInterpStringModel

-------`(pm.)modularInterpStringModel`----------
String instrument model with a modular body (see
[`modeInterpRes`](#pm.modeinterpres) and
<https://ccrma.stanford.edu/~rmichon/3dPrintingModeling/>).
#### Usage
```faust
modularInterpStringModel(length,pluckPosition,shape,scale,bodyExcitation,stringExcitation) : _
```
Where:
* `stringLength`: the length of the string in meters
* `pluckPosition`: pluck position (0-1) (1 is on the bridge)
* `shape`: shape of the resonator (0: square, 1: square with rounded corners, 2: round)
* `scale`: scale of the resonator (0: small, 1: medium, 2: large)
* `bodyExcitation`: excitation signal for the body
* `stringExcitation`: excitation signal for the string
#### Test
```faust
pm = library("physmodels.lib");
modularInterpStringModel_test = pm.modularInterpStringModel(0.9, 0.3, 1.0, 1.5, pm.impulseExcitation(button("body")), pm.impulseExcitation(button("string")));
```

---

## pm.modularInterpInstr

-------`(pm.)modularInterpInstr`----------
String instrument with a modular body (see
[`modeInterpRes`](#pm.modeinterpres) and
<https://ccrma.stanford.edu/~rmichon/3dPrintingModeling/>).
#### Usage
```faust
modularInterpInstr(stringLength,pluckPosition,shape,scale,gain,tapBody,triggerString) : _
```
Where:
* `stringLength`: the length of the string in meters
* `pluckPosition`: pluck position (0-1) (1 is on the bridge)
* `shape`: shape of the resonator (0: square, 1: square with rounded corners, 2: round)
* `scale`: scale of the resonator (0: small, 1: medium, 2: large)
* `gain`: of the string excitation
* `tapBody`: send an impulse in the body of the instrument where the string is connected (1 for on, 0 for off)
* `triggerString`: trigger signal for the string (1 for on, 0 for off)
#### Test
```faust
pm = library("physmodels.lib");
modularInterpInstr_test = pm.modularInterpInstr(0.9, 0.3, 1.0, 1.5, 0.8, button("body"), button("string"));
```

---

## pm.modularInterpInstr_ui_MIDI

-------`(pm.)modularInterpInstr_ui_MIDI`----------
Ready-to-use MIDI-enabled string instrument with a modular body (see
[`modeInterpRes`](#pm.modeinterpres) and
<https://ccrma.stanford.edu/~rmichon/3dPrintingModeling/>)
with built-in UI.
#### Usage
```faust
modularInterpInstr_ui_MIDI : _
```
#### Test
```faust
pm = library("physmodels.lib");
modularInterpInstr_ui_MIDI_test = pm.modularInterpInstr_ui_MIDI;
```

---

## pm.bowTable

-------`(pm.)bowTable`----------
Extremely basic bow table that can be used to implement a wide range of
bow types for many different bowed string instruments (violin, cello, etc.).
#### Usage
```faust
excitation : bowTable(offset,slope) : _
```
Where:
* `excitation`: an excitation signal
* `offset`: table offset
* `slope`: table slope
#### Test
```faust
pm = library("physmodels.lib");
bowTable_test = pm.bowTable(0.4, 0.1);
```

---

## pm.violinBowTable

-------`(pm.)violinBowTable`----------
Violin bow table based on [`bowTable`](#bowtable).
#### Usage
```faust
bowVelocity : violinBowTable(bowPressure) : _
```
Where:
* `bowVelocity`: velocity of the bow/excitation signal (0-1)
* `bowPressure`: bow pressure on the string (0-1)
#### Test
```faust
pm = library("physmodels.lib");
violinBowTable_test = pm.violinBowTable(0.4, 0.1);
```

---

## pm.bowInteraction

-------`(pm.)bowInteraction`----------
Bidirectional block implementing the interaction of a bow in a
[`chain`](#chain).
#### Usage
```faust
chain(... : stringSegment : bowInteraction(bowTable) : stringSegment : ...)
```
Where:
* `bowTable`: the bow table
#### Test
```faust
pm = library("physmodels.lib");
bowInteraction_test = pm.bowInteraction((0.4, 0.05));
```

---

## pm.violinBow

-------`(pm.)violinBow`----------
Bidirectional block implementing a violin bow and its interaction with
a string.
#### Usage
```faust
chain(... : stringSegment : violinBow(bowPressure,bowVelocity) : stringSegment : ...)
```
Where:
* `bowVelocity`: velocity of the bow / excitation signal (0-1)
* `bowPressure`: bow pressure on the string (0-1)
#### Test
```faust
pm = library("physmodels.lib");
violinBow_test = pm.violinBow(0.4, 0.05);
```

---

## pm.violinBowedString

-------`(pm.)violinBowedString`----------
Violin bowed string bidirectional block with controllable bow position.
Terminations are not implemented in this model.
#### Usage
```faust
chain(nuts : violinBowedString(stringLength,bowPressure,bowVelocity,bowPosition) : bridge)
```
Where:
* `stringLength`: the length of the string in meters
* `bowVelocity`: velocity of the bow / excitation signal (0-1)
* `bowPressure`: bow pressure on the string (0-1)
* `bowPosition`: the position of the bow on the string (0-1)
#### Test
```faust
pm = library("physmodels.lib");
violinBowedString_test = 0,0,0 : pm.violinBowedString(0.82, 0.35, pm.violinBow(0.4, 0.05), 0.15);
```

---

## pm.violinNuts

-------`(pm.)violinNuts`----------
Bidirectional block implementing simple violin nuts. This function is
based on [`bridgeFilter`](#bridgefilter).
#### Usage
```faust
chain(violinNuts : stringSegment : ...)
```
#### Test
```faust
pm = library("physmodels.lib");
violinNuts_test = 0,0,0 : pm.violinNuts;
```

---

## pm.violinBridge

-------`(pm.)violinBridge`----------
Bidirectional block implementing a simple violin bridge. This function is
based on [`bridgeFilter`](#bridgefilter).
#### Usage
```faust
chain(... : stringSegment : violinBridge
```
#### Test
```faust
pm = library("physmodels.lib");
violinBridge_test = 0,0,0 : pm.violinBridge;
```
TODO:
* reflectance is not implemented yet

---

## pm.violinBody

-------`(pm.)violinBody`----------
Bidirectional block implementing a simple violin body (just a simple
resonant lowpass filter).
#### Usage
```faust
chain(... : stringSegment : violinBridge : violinBody)
```
#### Test
```faust
pm = library("physmodels.lib");
violinBody_test = 0,0,0 : pm.violinBody;
```
TODO:
* reflectance is not implemented yet

---

## pm.violinModel

-------`(pm.)violinModel`----------
Ready-to-use simple violin physical model. This model implements a single
string. Additional strings should be created
by making a polyphonic application out of this function. Pitch is changed
by changing the length of the string (and not through a finger model).
#### Usage
```faust
violinModel(stringLength,bowPressure,bowVelocity,bridgeReflexion,
bridgeAbsorption,bowPosition) : _
```
Where:
* `stringLength`: the length of the string in meters
* `bowVelocity`: velocity of the bow / excitation signal (0-1)
* `bowPressure`: bow pressure on the string (0-1))
* `bowPosition`: the position of the bow on the string (0-1)
#### Test
```faust
pm = library("physmodels.lib");
violinModel_test = pm.violinModel(0.82, 0.35, pm.violinBow(0.4, 0.05), 0.15);
```

---

## pm.violin_ui

-------`(pm.)violin_ui`----------
Ready-to-use violin physical model with built-in UI.
#### Usage
```faust
violinModel_ui : _
```
#### Test
```faust
pm = library("physmodels.lib");
violin_ui_test = pm.violin_ui;
```

---

## pm.violin_ui_MIDI

-------`(pm.)violin_ui_MIDI`----------
Ready-to-use MIDI-enabled violin physical model with built-in UI.
#### Usage
```faust
violin_ui_MIDI : _
```
#### Test
```faust
pm = library("physmodels.lib");
violin_ui_MIDI_test = pm.violin_ui_MIDI;
```

---

## pm.openTube

-------`(pm.)openTube`----------
A tube segment without terminations (same as [`stringSegment`](#stringsegment)).
#### Usage
```faust
chain(A : openTube(maxLength,length) : B)
```
Where:
* `maxLength`: the maximum length of the tube in meters (should be static)
* `length`: the length of the tube in meters
#### Test
```faust
pm = library("physmodels.lib");
openTube_test = pm.openTube(0.9);
```

---

## pm.reedTable

-------`(pm.)reedTable`----------
Extremely basic reed table that can be used to implement a wide range of
single reed types for many different instruments (saxophone, clarinet, etc.).
#### Usage
```faust
excitation : reedTable(offeset,slope) : _
```
Where:
* `excitation`: an excitation signal
* `offset`: table offset
* `slope`: table slope
#### Test
```faust
pm = library("physmodels.lib");
reedTable_test = pm.reedTable(0.4, 0.2);
```

---

## pm.fluteJetTable

-------`(pm.)fluteJetTable`----------
Extremely basic flute jet table.
#### Usage
```faust
excitation : fluteJetTable : _
```
Where:
* `excitation`: an excitation signal
#### Test
```faust
pm = library("physmodels.lib");
fluteJetTable_test = pm.fluteJetTable(0.5);
```

---

## pm.brassLipsTable

-------`(pm.)brassLipsTable`----------
Simple brass lips/mouthpiece table. Since this implementation is very basic
and that the lips and tube of the instrument are coupled to each other, the
length of that tube must be provided here.
#### Usage
```faust
excitation : brassLipsTable(tubeLength,lipsTension) : _
```
Where:
* `excitation`: an excitation signal (can be DC)
* `tubeLength`: length in meters of the tube connected to the mouthpiece
* `lipsTension`: tension of the lips (0-1) (default: 0.5)
#### Test
```faust
pm = library("physmodels.lib");
brassLipsTable_test = pm.brassLipsTable(0.3, 0.2);
```

---

## pm.clarinetReed

-------`(pm.)clarinetReed`----------
Clarinet reed based on [`reedTable`](#reedtable) with controllable
stiffness.
#### Usage
```faust
excitation : clarinetReed(stiffness) : _
```
Where:
* `excitation`: an excitation signal
* `stiffness`: reed stiffness (0-1)
#### Test
```faust
pm = library("physmodels.lib");
clarinetReed_test = pm.clarinetReed(0.6, 0.4, 0.1);
```

---

## pm.clarinetMouthPiece

-------`(pm.)clarinetMouthPiece`----------
Bidirectional block implementing a clarinet mouthpiece as well as the various
interactions happening with traveling waves. This element is ready to be
plugged to a tube...
#### Usage
```faust
chain(clarinetMouthPiece(reedStiffness,pressure) : tube : etc.)
```
Where:
* `pressure`: the pressure of the air flow (DC) created by the virtual performer (0-1).
This can also be any kind of signal that will directly injected in the mouthpiece
(e.g., breath noise, etc.).
* `reedStiffness`: reed stiffness (0-1)
#### Test
```faust
pm = library("physmodels.lib");
clarinetMouthPiece_test = pm.clarinetMouthPiece(0.6, 0.4, 0.1);
```

---

## pm.brassLips

-------`(pm.)brassLips`----------
Bidirectional block implementing a brass mouthpiece as well as the various
interactions happening with traveling waves. This element is ready to be
plugged to a tube...
#### Usage
```faust
chain(brassLips(tubeLength,lipsTension,pressure) : tube : etc.)
```
Where:
* `tubeLength`: length in meters of the tube connected to the mouthpiece
* `lipsTension`: tension of the lips (0-1) (default: 0.5)
* `pressure`: the pressure of the air flow (DC) created by the virtual performer (0-1).
This can also be any kind of signal that will directly injected in the mouthpiece
(e.g., breath noise, etc.).
#### Test
```faust
pm = library("physmodels.lib");
brassLips_test = pm.brassLips(0.3, 0.2, 0.1);
```

---

## pm.fluteEmbouchure

-------`(pm.)fluteEmbouchure`----------
Bidirectional block implementing a flute embouchure as well as the various
interactions happening with traveling waves. This element is ready to be
plugged between tubes segments...
#### Usage
```faust
chain(... : tube : fluteEmbouchure(pressure) : tube : etc.)
```
Where:
* `pressure`: the pressure of the air flow (DC) created by the virtual
performer (0-1).
This can also be any kind of signal that will directly injected in the
mouthpiece (e.g., breath noise, etc.).
#### Test
```faust
pm = library("physmodels.lib");
fluteEmbouchure_test = pm.fluteEmbouchure(0.5, 0.3);
```

---

## pm.wBell

-------`(pm.)wBell`----------
Generic wind instrument bell bidirectional block that should be placed at
the end of a [`chain`](#chain).
#### Usage
```faust
chain(... : wBell(opening))
```
Where:
* `opening`: the "opening" of bell (0-1)
#### Test
```faust
pm = library("physmodels.lib");
wBell_test = pm.wBell(0.4, 0.6);
```

---

## pm.fluteHead

-------`(pm.)fluteHead`----------
Simple flute head implementing waves reflexion.
#### Usage
```faust
chain(fluteHead : tube : ...)
```
#### Test
```faust
pm = library("physmodels.lib");
fluteHead_test = pm.fluteHead(0.8, 0.4, 0.3);
```

---

## pm.fluteFoot

-------`(pm.)fluteFoot`----------
Simple flute foot implementing waves reflexion and dispersion.
#### Usage
```faust
chain(... : tube : fluteFoot)
```
#### Test
```faust
pm = library("physmodels.lib");
fluteFoot_test = pm.fluteFoot(0.8, 0.4, 0.3);
```

---

## pm.clarinetModel

-------`(pm.)clarinetModel`----------
A simple clarinet physical model without tone holes (pitch is changed by
changing the length of the tube of the instrument).
#### Usage
```faust
clarinetModel(length,pressure,reedStiffness,bellOpening) : _
```
Where:
* `tubeLength`: the length of the tube in meters
* `pressure`: the pressure of the air flow created by the virtual performer (0-1).
This can also be any kind of signal that will directly injected in the mouthpiece
(e.g., breath noise, etc.).
* `reedStiffness`: reed stiffness (0-1)
* `bellOpening`: the opening of bell (0-1)
#### Test
```faust
pm = library("physmodels.lib");
clarinetModel_test = pm.clarinetModel(0.9, 0.4, 0.3, 0.2);
```

---

## pm.clarinetModel_ui

-------`(pm.)clarinetModel_ui`----------
Same as [`clarinetModel`](#clarinetModel) but with a built-in UI. This function
doesn't implement a virtual "blower", thus `pressure` remains an argument here.
#### Usage
```faust
clarinetModel_ui(pressure) : _
```
Where:
* `pressure`: the pressure of the air flow created by the virtual performer (0-1).
This can also be any kind of signal that will be directly injected in the mouthpiece
(e.g., breath noise, etc.).
#### Test
```faust
pm = library("physmodels.lib");
clarinetModel_ui_test = pm.clarinetModel_ui;
```

---

## pm.clarinet_ui

-------`(pm.)clarinet_ui`----------
Ready-to-use clarinet physical model with built-in UI based on
[`clarinetModel`](#clarinetmodel).
#### Usage
```faust
clarinet_ui : _
```
#### Test
```faust
pm = library("physmodels.lib");
clarinet_ui_test = pm.clarinet_ui;
```

---

## pm.clarinet_ui_MIDI

-------`(pm.)clarinet_ui_MIDI`----------
Ready-to-use MIDI compliant clarinet physical model with built-in UI.
#### Usage
```faust
clarinet_ui_MIDI : _
```
#### Test
```faust
pm = library("physmodels.lib");
clarinet_ui_MIDI_test = pm.clarinet_ui_MIDI;
```

---

## pm.brassModel

-------`(pm.)brassModel`----------
A simple generic brass instrument physical model without pistons
(pitch is changed by changing the length of the tube of the instrument).
This model is kind of hard to control and might not sound very good if
bad parameters are given to it...
#### Usage
```faust
brassModel(tubeLength,lipsTension,mute,pressure) : _
```
Where:
* `tubeLength`: the length of the tube in meters
* `lipsTension`: tension of the lips (0-1) (default: 0.5)
* `mute`: mute opening at the end of the instrument (0-1) (default: 0.5)
* `pressure`: the pressure of the air flow created by the virtual performer (0-1).
This can also be any kind of signal that will directly injected in the mouthpiece
(e.g., breath noise, etc.).
#### Test
```faust
pm = library("physmodels.lib");
brassModel_test = pm.brassModel(0.9, 0.4, 0.2, 0.6);
```

---

## pm.brassModel_ui

-------`(pm.)brassModel_ui`----------
Same as [`brassModel`](#brassModel) but with a built-in UI. This function
doesn't implement a virtual "blower", thus `pressure` remains an argument here.
#### Usage
```faust
brassModel_ui(pressure) : _
```
Where:
* `pressure`: the pressure of the air flow created by the virtual performer (0-1).
This can also be any kind of signal that will be directly injected in the mouthpiece
(e.g., breath noise, etc.).
#### Test
```faust
pm = library("physmodels.lib");
brassModel_ui_test = pm.brassModel_ui;
```

---

## pm.brass_ui

-------`(pm.)brass_ui`----------
Ready-to-use brass instrument physical model with built-in UI based on
[`brassModel`](#brassmodel).
#### Usage
```faust
brass_ui : _
```
#### Test
```faust
pm = library("physmodels.lib");
brass_ui_test = pm.brass_ui;
```

---

## pm.brass_ui_MIDI

-------`(pm.)brass_ui_MIDI`----------
Ready-to-use MIDI-controllable brass instrument physical model with built-in UI.
#### Usage
```faust
brass_ui_MIDI : _
```
#### Test
```faust
pm = library("physmodels.lib");
brass_ui_MIDI_test = pm.brass_ui_MIDI;
```

---

## pm.fluteModel

-------`(pm.)fluteModel`----------
A simple generic flute instrument physical model without tone holes
(pitch is changed by changing the length of the tube of the instrument).
#### Usage
```faust
fluteModel(tubeLength,mouthPosition,pressure) : _
```
Where:
* `tubeLength`: the length of the tube in meters
* `mouthPosition`: position of the mouth on the embouchure (0-1) (default: 0.5)
* `pressure`: the pressure of the air flow created by the virtual performer (0-1).
This can also be any kind of signal that will directly injected in the mouthpiece
(e.g., breath noise, etc.).
#### Test
```faust
pm = library("physmodels.lib");
fluteModel_test = pm.fluteModel(0.9, 0.4, 0.6);
```
TODO: this model is out of tune and we're not really sure why

---

## pm.fluteModel_ui

-------`(pm.)fluteModel_ui`----------
Same as [`fluteModel`](#fluteModel) but with a built-in UI. This function
doesn't implement a virtual "blower", thus `pressure` remains an argument here.
#### Usage
```faust
fluteModel_ui(pressure) : _
```
Where:
* `pressure`: the pressure of the air flow created by the virtual performer (0-1).
This can also be any kind of signal that will be directly injected in the mouthpiece
(e.g., breath noise, etc.).
#### Test
```faust
pm = library("physmodels.lib");
fluteModel_ui_test = pm.fluteModel_ui;
```

---

## pm.flute_ui

-------`(pm.)flute_ui`----------
Ready-to-use flute physical model with built-in UI based on
[`fluteModel`](#flutemodel).
#### Usage
```faust
flute_ui : _
```
#### Test
```faust
pm = library("physmodels.lib");
flute_ui_test = pm.flute_ui;
```

---

## pm.flute_ui_MIDI

-------`(pm.)flute_ui_MIDI`----------
Ready-to-use MIDI-controllable flute physical model with built-in UI.
#### Usage
```faust
flute_ui_MIDI : _
```
#### Test
```faust
pm = library("physmodels.lib");
flute_ui_MIDI_test = pm.flute_ui_MIDI;
```

---

## pm.impulseExcitation

-------`(pm.)impulseExcitation`--------------
Creates an impulse excitation of one sample.
#### Usage
```faust
gate = button('gate');
impulseExcitation(gate) : chain;
```
Where:
* `gate`: a gate button
#### Test
```faust
pm = library("physmodels.lib");
impulseExcitation_test = pm.impulseExcitation(button("gate"));
```

---

## pm.strikeModel

-------`(pm.)strikeModel`--------------
Creates a filtered noise excitation.
#### Usage
```faust
gate = button('gate');
strikeModel(LPcutoff,HPcutoff,sharpness,gain,gate) : chain;
```
Where:
* `HPcutoff`: highpass cutoff frequency
* `LPcutoff`: lowpass cutoff frequency
* `sharpness`: sharpness of the attack and release (0-1)
* `gain`: gain of the excitation
* `gate`: a gate button/trigger signal (0/1)
#### Test
```faust
pm = library("physmodels.lib");
strikeModel_test = pm.strikeModel(200, 4000, 0.5, 0.8, button("gate"));
```

---

## pm.strike

-------`(pm.)strike`--------------
Strikes generator with controllable excitation position.
#### Usage
```faust
gate = button('gate');
strike(exPos,sharpness,gain,gate) : chain;
```
Where:
* `exPos`: excitation position wiht 0: for max low freqs and 1: for max high
freqs. So, on membrane for example, 0 would be the middle and 1 the edge
* `sharpness`: sharpness of the attack and release (0-1)
* `gain`: gain of the excitation
* `gate`: a gate button/trigger signal (0/1)
#### Test
```faust
pm = library("physmodels.lib");
strike_test = pm.strike(0.4, 0.5, 0.8, button("gate"));
```

---

## pm.pluckString

-------`(pm.)pluckString`--------------
Creates a plucking excitation signal.
#### Usage
```faust
trigger = button('gate');
pluckString(stringLength,cutoff,maxFreq,sharpness,trigger)
```
Where:
* `stringLength`: length of the string to pluck
* `cutoff`: cutoff ratio (1 for default)
* `maxFreq`: max frequency ratio (1 for default)
* `sharpness`: sharpness of the attack and release (1 for default)
* `gain`: gain of the excitation (0-1)
* `trigger`: trigger signal (1 for on, 0 for off)
#### Test
```faust
pm = library("physmodels.lib");
pluckString_test = pm.pluckString(0.9, 1, 1, 1, 0.6, button("gate"));
```

---

## pm.blower

-------`(pm.)blower`--------------
A virtual blower creating a DC signal with some breath noise in it.
#### Usage
```faust
blower(pressure,breathGain,breathCutoff) : _
```
Where:
* `pressure`: pressure (0-1)
* `breathGain`: breath noise gain (0-1) (recommended: 0.005)
* `breathCutoff`: breath cuttoff frequency (Hz) (recommended: 2000)
#### Test
```faust
pm = library("physmodels.lib");
blower_test = pm.blower(0.5, 0.05, 2000, 5, 0.2);
```

---

## pm.blower_ui

-------`(pm.)blower_ui`--------------
Same as [`blower`](#blower) but with a built-in UI.
#### Usage
```faust
blower : somethingToBeBlown
```
#### Test
```faust
pm = library("physmodels.lib");
blower_ui_test = pm.blower_ui;
```

---

## pm.djembeModel

-------`(pm.)djembeModel`----------
Dirt-simple djembe modal physical model. Mode parameters are empirically
calculated and don't correspond to any measurements or 3D model. They
kind of sound good though :).
#### Usage
```faust
excitation : djembeModel(freq)
```
Where:
* `excitation`: excitation signal
* `freq`: fundamental frequency of the bar
#### Test
```faust
pm = library("physmodels.lib");
djembeModel_test = pm.djembeModel(110);
```

---

## pm.djembe

-------`(pm.)djembe`----------
Dirt-simple djembe modal physical model. Mode parameters are empirically
calculated and don't correspond to any measurements or 3D model. They
kind of sound good though :).
This model also implements a virtual "exciter".
#### Usage
```faust
djembe(freq,strikePosition,strikeSharpness,gain,trigger)
```
Where:
* `freq`: fundamental frequency of the model
* `strikePosition`: strike position (0 for the middle of the membrane and
1 for the edge)
* `strikeSharpness`: sharpness of the strike (0-1, default: 0.5)
* `gain`: gain of the strike
* `trigger`: trigger signal (0: off, 1: on)
#### Test
```faust
pm = library("physmodels.lib");
djembe_test = pm.djembe(110, 0.3, 0.5, 0.8, button("gate"));
```

---

## pm.djembe_ui_MIDI

-------`(pm.)djembe_ui_MIDI`----------
Simple MIDI controllable djembe physical model with built-in UI.
#### Usage
```faust
djembe_ui_MIDI : _
```
#### Test
```faust
pm = library("physmodels.lib");
djembe_ui_MIDI_test = pm.djembe_ui_MIDI;
```

---

## pm.marimbaBarModel

-------`(pm.)marimbaBarModel`----------
Generic marimba tone bar modal model.
This model was generated using
`mesh2faust` from a 3D CAD model of a marimba tone bar
(`libraries/modalmodels/marimbaBar`). The corresponding CAD model is that
of a C2 tone bar (original fundamental frequency: ~65Hz). While
`marimbaBarModel` allows to translate the harmonic content of the generated
sound by providing a frequency (`freq`), mode transposition has limits and
the model will sound less and less like a marimba tone bar as it
diverges from C2. To make an accurate model of a marimba, we'd want to have
an independent model for each bar...
This model contains 5 excitation positions going linearly from the center
bottom to the center top of the bar. Obviously, a model with more excitation
position could be regenerated using `mesh2faust`.
#### Usage
```faust
excitation : marimbaBarModel(freq,exPos,t60,t60DecayRatio,t60DecaySlope)
```
Where:
* `excitation`: excitation signal
* `freq`: fundamental frequency of the bar
* `exPos`: excitation position (0-4)
* `t60`: T60 in seconds (recommended value: 0.1)
* `t60DecayRatio`: T60 decay ratio (recommended value: 1)
* `t60DecaySlope`: T60 decay slope (recommended value: 5)
#### Test
```faust
pm = library("physmodels.lib");
marimbaBarModel_test = pm.marimbaBarModel(220);
```

---

## pm.marimbaResTube

-------`(pm.)marimbaResTube`----------
Simple marimba resonance tube.
#### Usage
```faust
marimbaResTube(tubeLength,excitation)
```
Where:
* `tubeLength`: the length of the tube in meters
* `excitation`: the excitation signal (audio in)
#### Test
```faust
pm = library("physmodels.lib");
marimbaResTube_test = pm.marimbaResTube(220);
```

---

## pm.marimbaModel

-------`(pm.)marimbaModel`----------
Simple marimba physical model implementing a single tone bar connected to
tube. This model is scalable and can be adapted to any size of bar/tube
(see [`marimbaBarModel`](#marimbabarmodel) to know more about the
limitations of this type of system).
#### Usage
```faust
excitation : marimbaModel(freq,exPos) : _
```
Where:
* `excitation`: the excitation signal
* `freq`: the frequency of the bar/tube couple
* `exPos`: excitation position (0-4)
#### Test
```faust
pm = library("physmodels.lib");
marimbaModel_test = pm.marimbaModel(220);
```

---

## pm.marimba

-------`(pm.)marimba`----------
Simple marimba physical model implementing a single tone bar connected to
tube. This model is scalable and can be adapted to any size of bar/tube
(see [`marimbaBarModel`](#marimbabarmodel) to know more about the
limitations of this type of system).
This function also implement a virtual exciter to drive the model.
#### Usage
```faust
marimba(freq,strikePosition,strikeCutoff,strikeSharpness,gain,trigger) : _
```
Where:
* `freq`: the frequency of the bar/tube couple
* `strikePosition`: strike position (0-4)
* `strikeCutoff`: cuttoff frequency of the strike genarator (recommended: ~7000Hz)
* `strikeSharpness`: sharpness of the strike (recommended: ~0.25)
* `gain`: gain of the strike (0-1)
* `trigger` signal (0: off, 1: on)
#### Test
```faust
pm = library("physmodels.lib");
marimba_test = pm.marimba(220, 0.4, 1, 0.5, 0.8, button("gate"));
```

---

## pm.marimba_ui_MIDI

-------`(pm.)marimba_ui_MIDI`----------
Simple MIDI controllable marimba physical model with built-in UI
implementing a single tone bar connected to
tube. This model is scalable and can be adapted to any size of bar/tube
(see [`marimbaBarModel`](#marimbabarmodel) to know more about the
limitations of this type of system).
#### Usage
```faust
marimba_ui_MIDI : _
```
#### Test
```faust
pm = library("physmodels.lib");
marimba_ui_MIDI_test = pm.marimba_ui_MIDI;
```

---

## pm.churchBellModel

-------`(pm.)churchBellModel`----------
Generic church bell modal model generated by `mesh2faust` from
`libraries/modalmodels/churchBell`.
Modeled after T. Rossing and R. Perrin, Vibrations of Bells, Applied
Acoustics 2, 1987.
Model height is 301 mm.
This model contains 7 excitation positions going linearly from the
bottom to the top of the bell. Obviously, a model with more excitation
position could be regenerated using `mesh2faust`.
#### Usage
```faust
excitation : churchBellModel(nModes,exPos,t60,t60DecayRatio,t60DecaySlope)
```
Where:
* `excitation`: the excitation signal
* `nModes`: number of synthesized modes (max: 50)
* `exPos`: excitation position (0-6)
* `t60`: T60 in seconds (recommended value: 0.1)
* `t60DecayRatio`: T60 decay ratio (recommended value: 1)
* `t60DecaySlope`: T60 decay slope (recommended value: 5)
#### Test
```faust
pm = library("physmodels.lib");
churchBellModel_test = pm.churchBellModel(110);
```

---

## pm.churchBell

-------`(pm.)churchBell`----------
Generic church bell modal model.
Modeled after T. Rossing and R. Perrin, Vibrations of Bells, Applied
Acoustics 2, 1987.
Model height is 301 mm.
This model contains 7 excitation positions going linearly from the
bottom to the top of the bell. Obviously, a model with more excitation
position could be regenerated using `mesh2faust`.
This function also implement a virtual exciter to drive the model.
#### Usage
```faust
churchBell(strikePosition,strikeCutoff,strikeSharpness,gain,trigger) : _
```
Where:
* `strikePosition`: strike position (0-6)
* `strikeCutoff`: cuttoff frequency of the strike genarator (recommended: ~7000Hz)
* `strikeSharpness`: sharpness of the strike (recommended: ~0.25)
* `gain`: gain of the strike (0-1)
* `trigger` signal (0: off, 1: on)
#### Test
```faust
pm = library("physmodels.lib");
churchBell_test = pm.churchBell(0.4, 2000, 0.5, 0.8, button("gate"));
```

---

## pm.churchBell_ui

-------`(pm.)churchBell_ui`----------
Church bell physical model based on [`churchBell`](#pmchurchbell) with
built-in UI.
#### Usage
```faust
churchBell_ui : _
```
#### Test
```faust
pm = library("physmodels.lib");
churchBell_ui_test = pm.churchBell_ui;
```

---

## pm.englishBellModel

-------`(pm.)englishBellModel`----------
English church bell modal model generated by `mesh2faust` from
`libraries/modalmodels/englishBell`.
Modeled after D.Bartocha and Baron, Influence of Tin Bronze Melting and
Pouring Parameters on Its Properties and Bell' Tone, Archives of Foundry
Engineering, 2016.
Model height is 1 m.
This model contains 7 excitation positions going linearly from the
bottom to the top of the bell. Obviously, a model with more excitation
position could be regenerated using `mesh2faust`.
#### Usage
```faust
excitation : englishBellModel(nModes,exPos,t60,t60DecayRatio,t60DecaySlope)
```
Where:
* `excitation`: the excitation signal
* `nModes`: number of synthesized modes (max: 50)
* `exPos`: excitation position (0-6)
* `t60`: T60 in seconds (recommended value: 0.1)
* `t60DecayRatio`: T60 decay ratio (recommended value: 1)
* `t60DecaySlope`: T60 decay slope (recommended value: 5)
#### Test
```faust
pm = library("physmodels.lib");
englishBellModel_test = pm.englishBellModel(110);
```

---

## pm.englishBell

-------`(pm.)englishBell`----------
English church bell modal model.
Modeled after D.Bartocha and Baron, Influence of Tin Bronze Melting and
Pouring Parameters on Its Properties and Bell' Tone, Archives of Foundry
Engineering, 2016.
Model height is 1 m.
This model contains 7 excitation positions going linearly from the
bottom to the top of the bell. Obviously, a model with more excitation
position could be regenerated using `mesh2faust`.
This function also implement a virtual exciter to drive the model.
#### Usage
```faust
englishBell(strikePosition,strikeCutoff,strikeSharpness,gain,trigger) : _
```
Where:
* `strikePosition`: strike position (0-6)
* `strikeCutoff`: cuttoff frequency of the strike genarator (recommended: ~7000Hz)
* `strikeSharpness`: sharpness of the strike (recommended: ~0.25)
* `gain`: gain of the strike (0-1)
* `trigger` signal (0: off, 1: on)
#### Test
```faust
pm = library("physmodels.lib");
englishBell_test = pm.englishBell(0.4, 2000, 0.5, 0.8, button("gate"));
```

---

## pm.englishBell_ui

-------`(pm.)englishBell_ui`----------
English church bell physical model based on [`englishBell`](#pmenglishbell) with
built-in UI.
#### Usage
```faust
englishBell_ui : _
```
#### Test
```faust
pm = library("physmodels.lib");
englishBell_ui_test = pm.englishBell_ui;
```

---

## pm.frenchBellModel

-------`(pm.)frenchBellModel`----------
French church bell modal model generated by `mesh2faust` from
`libraries/modalmodels/frenchBell`.
Modeled after D.Bartocha and Baron, Influence of Tin Bronze Melting and
Pouring Parameters on Its Properties and Bell' Tone, Archives of Foundry
Engineering, 2016.
Model height is 1 m.
This model contains 7 excitation positions going linearly from the
bottom to the top of the bell. Obviously, a model with more excitation
position could be regenerated using `mesh2faust`.
#### Usage
```faust
excitation : frenchBellModel(nModes,exPos,t60,t60DecayRatio,t60DecaySlope)
```
Where:
* `excitation`: the excitation signal
* `nModes`: number of synthesized modes (max: 50)
* `exPos`: excitation position (0-6)
* `t60`: T60 in seconds (recommended value: 0.1)
* `t60DecayRatio`: T60 decay ratio (recommended value: 1)
* `t60DecaySlope`: T60 decay slope (recommended value: 5)
#### Test
```faust
pm = library("physmodels.lib");
frenchBellModel_test = pm.frenchBellModel(110);
```

---

## pm.frenchBell

-------`(pm.)frenchBell`----------
French church bell modal model.
Modeled after D.Bartocha and Baron, Influence of Tin Bronze Melting and
Pouring Parameters on Its Properties and Bell' Tone, Archives of Foundry
Engineering, 2016.
Model height is 1 m.
This model contains 7 excitation positions going linearly from the
bottom to the top of the bell. Obviously, a model with more excitation
position could be regenerated using `mesh2faust`.
This function also implement a virtual exciter to drive the model.
#### Usage
```faust
frenchBell(strikePosition,strikeCutoff,strikeSharpness,gain,trigger) : _
```
Where:
* `strikePosition`: strike position (0-6)
* `strikeCutoff`: cuttoff frequency of the strike genarator (recommended: ~7000Hz)
* `strikeSharpness`: sharpness of the strike (recommended: ~0.25)
* `gain`: gain of the strike (0-1)
* `trigger` signal (0: off, 1: on)
#### Test
```faust
pm = library("physmodels.lib");
frenchBell_test = pm.frenchBell(0.4, 2000, 0.5, 0.8, button("gate"));
```

---

## pm.frenchBell_ui

-------`(pm.)frenchBell_ui`----------
French church bell physical model based on [`frenchBell`](#pmfrenchbell) with
built-in UI.
#### Usage
```faust
frenchBell_ui : _
```
#### Test
```faust
pm = library("physmodels.lib");
frenchBell_ui_test = pm.frenchBell_ui;
```

---

## pm.germanBellModel

-------`(pm.)germanBellModel`----------
German church bell modal model generated by `mesh2faust` from
`libraries/modalmodels/germanBell`.
Modeled after D.Bartocha and Baron, Influence of Tin Bronze Melting and
Pouring Parameters on Its Properties and Bell' Tone, Archives of Foundry
Engineering, 2016.
Model height is 1 m.
This model contains 7 excitation positions going linearly from the
bottom to the top of the bell. Obviously, a model with more excitation
position could be regenerated using `mesh2faust`.
#### Usage
```faust
excitation : germanBellModel(nModes,exPos,t60,t60DecayRatio,t60DecaySlope)
```
Where:
* `excitation`: the excitation signal
* `nModes`: number of synthesized modes (max: 50)
* `exPos`: excitation position (0-6)
* `t60`: T60 in seconds (recommended value: 0.1)
* `t60DecayRatio`: T60 decay ratio (recommended value: 1)
* `t60DecaySlope`: T60 decay slope (recommended value: 5)
#### Test
```faust
pm = library("physmodels.lib");
germanBellModel_test = pm.germanBellModel(110);
```

---

## pm.germanBell

-------`(pm.)germanBell`----------
German church bell modal model.
Modeled after D.Bartocha and Baron, Influence of Tin Bronze Melting and
Pouring Parameters on Its Properties and Bell' Tone, Archives of Foundry
Engineering, 2016.
Model height is 1 m.
This model contains 7 excitation positions going linearly from the
bottom to the top of the bell. Obviously, a model with more excitation
position could be regenerated using `mesh2faust`.
This function also implement a virtual exciter to drive the model.
#### Usage
```faust
germanBell(strikePosition,strikeCutoff,strikeSharpness,gain,trigger) : _
```
Where:
* `strikePosition`: strike position (0-6)
* `strikeCutoff`: cuttoff frequency of the strike genarator (recommended: ~7000Hz)
* `strikeSharpness`: sharpness of the strike (recommended: ~0.25)
* `gain`: gain of the strike (0-1)
* `trigger` signal (0: off, 1: on)
#### Test
```faust
pm = library("physmodels.lib");
germanBell_test = pm.germanBell(0.4, 2000, 0.5, 0.8, button("gate"));
```

---

## pm.germanBell_ui

-------`(pm.)germanBell_ui`----------
German church bell physical model based on [`germanBell`](#pmgermanbell) with
built-in UI.
#### Usage
```faust
germanBell_ui : _
```
#### Test
```faust
pm = library("physmodels.lib");
germanBell_ui_test = pm.germanBell_ui;
```

---

## pm.russianBellModel

-------`(pm.)russianBellModel`----------
Russian church bell modal model generated by `mesh2faust` from
`libraries/modalmodels/russianBell`.
Modeled after D.Bartocha and Baron, Influence of Tin Bronze Melting and
Pouring Parameters on Its Properties and Bell' Tone, Archives of Foundry
Engineering, 2016.
Model height is 2 m.
This model contains 7 excitation positions going linearly from the
bottom to the top of the bell. Obviously, a model with more excitation
position could be regenerated using `mesh2faust`.
#### Usage
```faust
excitation : russianBellModel(nModes,exPos,t60,t60DecayRatio,t60DecaySlope)
```
Where:
* `excitation`: the excitation signal
* `nModes`: number of synthesized modes (max: 50)
* `exPos`: excitation position (0-6)
* `t60`: T60 in seconds (recommended value: 0.1)
* `t60DecayRatio`: T60 decay ratio (recommended value: 1)
* `t60DecaySlope`: T60 decay slope (recommended value: 5)
#### Test
```faust
pm = library("physmodels.lib");
russianBellModel_test = pm.russianBellModel(110);
```

---

## pm.russianBell

-------`(pm.)russianBell`----------
Russian church bell modal model.
Modeled after D.Bartocha and Baron, Influence of Tin Bronze Melting and
Pouring Parameters on Its Properties and Bell' Tone, Archives of Foundry
Engineering, 2016.
Model height is 2 m.
This model contains 7 excitation positions going linearly from the
bottom to the top of the bell. Obviously, a model with more excitation
position could be regenerated using `mesh2faust`.
This function also implement a virtual exciter to drive the model.
#### Usage
```faust
russianBell(strikePosition,strikeCutoff,strikeSharpness,gain,trigger) : _
```
Where:
* `strikePosition`: strike position (0-6)
* `strikeCutoff`: cuttoff frequency of the strike genarator (recommended: ~7000Hz)
* `strikeSharpness`: sharpness of the strike (recommended: ~0.25)
* `gain`: gain of the strike (0-1)
* `trigger` signal (0: off, 1: on)
#### Test
```faust
pm = library("physmodels.lib");
russianBell_test = pm.russianBell(0.4, 2000, 0.5, 0.8, button("gate"));
```

---

## pm.russianBell_ui

-------`(pm.)russianBell_ui`----------
Russian church bell physical model based on [`russianBell`](#pmrussianbell) with
built-in UI.
#### Usage
```faust
russianBell_ui : _
```
#### Test
```faust
pm = library("physmodels.lib");
russianBell_ui_test = pm.russianBell_ui;
```

---

## pm.standardBellModel

-------`(pm.)standardBellModel`----------
Standard church bell modal model generated by `mesh2faust` from
`libraries/modalmodels/standardBell`.
Modeled after T. Rossing and R. Perrin, Vibrations of Bells, Applied
Acoustics 2, 1987.
Model height is 1.8 m.
This model contains 7 excitation positions going linearly from the
bottom to the top of the bell. Obviously, a model with more excitation
position could be regenerated using `mesh2faust`.
#### Usage
```faust
excitation : standardBellModel(nModes,exPos,t60,t60DecayRatio,t60DecaySlope)
```
Where:
* `excitation`: the excitation signal
* `nModes`: number of synthesized modes (max: 50)
* `exPos`: excitation position (0-6)
* `t60`: T60 in seconds (recommended value: 0.1)
* `t60DecayRatio`: T60 decay ratio (recommended value: 1)
* `t60DecaySlope`: T60 decay slope (recommended value: 5)
#### Test
```faust
pm = library("physmodels.lib");
standardBellModel_test = pm.standardBellModel(110);
```

---

## pm.standardBell

-------`(pm.)standardBell`----------
Standard church bell modal model.
Modeled after T. Rossing and R. Perrin, Vibrations of Bells, Applied
Acoustics 2, 1987.
Model height is 1.8 m.
This model contains 7 excitation positions going linearly from the
bottom to the top of the bell. Obviously, a model with more excitation
position could be regenerated using `mesh2faust`.
This function also implement a virtual exciter to drive the model.
#### Usage
```faust
standardBell(strikePosition,strikeCutoff,strikeSharpness,gain,trigger) : _
```
Where:
* `strikePosition`: strike position (0-6)
* `strikeCutoff`: cuttoff frequency of the strike genarator (recommended: ~7000Hz)
* `strikeSharpness`: sharpness of the strike (recommended: ~0.25)
* `gain`: gain of the strike (0-1)
* `trigger` signal (0: off, 1: on)
#### Test
```faust
pm = library("physmodels.lib");
standardBell_test = pm.standardBell(0.4, 2000, 0.5, 0.8, button("gate"));
```

---

## pm.standardBell_ui

-------`(pm.)standardBell_ui`----------
Standard church bell physical model based on [`standardBell`](#pmstandardbell) with
built-in UI.
#### Usage
```faust
standardBell_ui : _
```
#### Test
```faust
pm = library("physmodels.lib");
standardBell_ui_test = pm.standardBell_ui;
```

---

## pm.formantValues

-------`(pm.)formantValues`----------
Formant data values in an environment.
The formant data used here come from the CSOUND manual
<http://www.csounds.com/manual/html/>.
#### Usage
```faust
ba.take(j+1,formantValues.f(i)) : _
ba.take(j+1,formantValues.g(i)) : _
ba.take(j+1,formantValues.bw(i)) : _
```
Where:
* `i`: formant number
* `j`: (voiceType*nFormants)+vowel
* `voiceType`: the voice type (0: alto, 1: bass, 2: countertenor, 3:
soprano, 4: tenor)
* `vowel`: the vowel (0: a, 1: e, 2: i, 3: o, 4: u)
#### Test
```faust
pm = library("physmodels.lib");
formantValues_test = pm.formantValues.f(0);
```

---

## pm.voiceGender

--------------`(pm.)voiceGender`-----------------
Calculate the gender for the provided `voiceType` value. (0: male, 1: female)
#### Usage
```faust
voiceGender(voiceType) : _
```
Where:
* `voiceType`: the voice type (0: alto, 1: bass, 2: countertenor, 3: soprano, 4: tenor)
#### Test
```faust
pm = library("physmodels.lib");
voiceGender_test = pm.voiceGender(0.5);
```

---

## pm.skirtWidthMultiplier

-----------`(pm.)skirtWidthMultiplier`------------
Calculates value to multiply bandwidth to obtain `skirtwidth`
for a Fof filter.
#### Usage
```faust
skirtWidthMultiplier(vowel,freq,gender) : _
```
Where:
* `vowel`: the vowel (0: a, 1: e, 2: i, 3: o, 4: u)
* `freq`: the fundamental frequency of the excitation signal
* `gender`: gender of the voice used in the fof filter (0: male, 1: female)
#### Test
```faust
pm = library("physmodels.lib");
skirtWidthMultiplier_test = pm.skirtWidthMultiplier(0.5);
```

---

## pm.autobendFreq

--------------`(pm.)autobendFreq`-----------------
Autobends the center frequencies of formants 1 and 2 based on
the fundamental frequency of the excitation signal and leaves
all other formant frequencies unchanged. Ported from `chant-lib`.
#### Usage
```faust
_ : autobendFreq(n,freq,voiceType) : _
```
Where:
* `n`: formant index
* `freq`: the fundamental frequency of the excitation signal
* `voiceType`: the voice type (0: alto, 1: bass, 2: countertenor, 3: soprano, 4: tenor)
* input is the center frequency of the corresponding formant
#### Test
```faust
pm = library("physmodels.lib");
autobendFreq_test = pm.autobendFreq(440, 0.5);
```
#### References
* <https://ccrma.stanford.edu/~rmichon/chantLib/>.

---

## pm.vocalEffort

--------------`(pm.)vocalEffort`-----------------
Changes the gains of the formants based on the fundamental
frequency of the excitation signal. Higher formants are
reinforced for higher fundamental frequencies.
Ported from `chant-lib`.
#### Usage
```faust
_ : vocalEffort(freq,gender) : _
```
Where:
* `freq`: the fundamental frequency of the excitation signal
* `gender`: the gender of the voice type (0: male, 1: female)
* input is the linear amplitude of the formant
#### Test
```faust
pm = library("physmodels.lib");
vocalEffort_test = pm.vocalEffort(0.6);
```
#### References
* <https://ccrma.stanford.edu/~rmichon/chantLib/>.

---

## pm.fof

-------------------------`(pm.)fof`--------------------------
Function to generate a single Formant-Wave-Function.
#### Usage
```faust
_ : fof(fc,bw,a,g) : _
```
Where:
* `fc`: formant center frequency,
* `bw`: formant bandwidth (Hz),
* `sw`: formant skirtwidth (Hz)
* `g`: linear scale factor (g=1 gives 0dB amplitude response at fc)
* input is an impulse signal to excite filter
#### Test
```faust
pm = library("physmodels.lib");
fof_test = pm.fof(0.3, 440, 880, 0.5);
```
#### References
* <https://ccrma.stanford.edu/~mjolsen/pdfs/smc2016_MOlsenFOF.pdf>.

---

## pm.fofSH

-------------------------`(pm.)fofSH`-------------------------
FOF with sample and hold used on `bw` and a parameter
used in the filter-cycling FOF function `fofCycle`.
#### Usage
```faust
_ : fofSH(fc,bw,a,g) : _
```
Where: all parameters same as for [`fof`](#fof)
#### Test
```faust
pm = library("physmodels.lib");
fofSH_test = pm.fofSH(0.3, 440, 880, 0.5);
```
#### References
* <https://ccrma.stanford.edu/~mjolsen/pdfs/smc2016_MOlsenFOF.pdf>.

---

## pm.fofCycle

----------------------`(pm.)fofCycle`-------------------------
FOF implementation where time-varying filter parameter noise is
mitigated by using a cycle of `n` sample and hold FOF filters.
#### Usage
```faust
_ : fofCycle(fc,bw,a,g,n) : _
```
Where:
* `n`: the number of FOF filters to cycle through
* all other parameters are same as for [`fof`](#fof)
#### Test
```faust
pm = library("physmodels.lib");
fofCycle_test = pm.fofCycle(0.3, 440, 880, 0.5, 0.2);
```
#### References
* <https://ccrma.stanford.edu/~mjolsen/pdfs/smc2016_MOlsenFOF.pdf>.

---

## pm.fofSmooth

----------------------`(pm.)fofSmooth`-------------------------
FOF implementation where time-varying filter parameter
noise is mitigated by lowpass filtering the filter
parameters `bw` and `a` with [smooth](#smooth).
#### Usage
```faust
_ : fofSmooth(fc,bw,sw,g,tau) : _
```
Where:
* `tau`: the desired smoothing time constant in seconds
* all other parameters are same as for [`fof`](#fof)
#### Test
```faust
pm = library("physmodels.lib");
fofSmooth_test = pm.fofSmooth(0.3, 440, 880, 0.5, 0.2);
```

---

## pm.formantFilterFofCycle

-------`(pm.)formantFilterFofCycle`--------------
Formant filter based on a single FOF filter.
Formant parameters are linearly interpolated allowing to go smoothly from
one vowel to another. A cycle of `n` fof filters with sample-and-hold is
used so that the fof filter parameters can be varied in realtime.
This technique is more robust but more computationally expensive than
[`formantFilterFofSmooth`](#formantFilterFofSmooth).Voice type can be
selected but must correspond to
the frequency range of the provided source to be realistic.
#### Usage
```faust
_ : formantFilterFofCycle(voiceType,vowel,nFormants,i,freq) : _
```
Where:
* `voiceType`: the voice type (0: alto, 1: bass, 2: countertenor,
3: soprano, 4: tenor)
* `vowel`: the vowel (0: a, 1: e, 2: i, 3: o, 4: u)
* `nFormants`: number of formant regions in frequency domain, typically 5
* `i`: formant number (i.e. 0 - 4) used to index formant data value arrays
* `freq`: fundamental frequency of excitation signal. Used to calculate
rise time of envelope
#### Test
```faust
pm = library("physmodels.lib");
formantFilterFofCycle_test = pm.formantFilterFofCycle(0, 0, 5, 0, 200);
```

---

## pm.formantFilterFofSmooth

-------`(pm.)formantFilterFofSmooth`--------------
Formant filter based on a single FOF filter.
Formant parameters are linearly interpolated allowing to go smoothly from
one vowel to another. Fof filter parameters are lowpass filtered
to mitigate possible noise from varying them in realtime.
Voice type can be selected but must correspond to
the frequency range of the provided source to be realistic.
#### Usage
```faust
_ : formantFilterFofSmooth(voiceType,vowel,nFormants,i,freq) : _
```
Where:
* `voiceType`: the voice type (0: alto, 1: bass, 2: countertenor,
3: soprano, 4: tenor)
* `vowel`: the vowel (0: a, 1: e, 2: i, 3: o, 4: u)
* `nFormants`: number of formant regions in frequency domain, typically 5
* `i`: formant number (i.e. 1 - 5) used to index formant data value arrays
* `freq`: fundamental frequency of excitation signal. Used to calculate
rise time of envelope
#### Test
```faust
pm = library("physmodels.lib");
formantFilterFofSmooth_test = pm.formantFilterFofSmooth(0, 0, 5, 0, 200);
```

---

## pm.formantFilterBP

-------`(pm.)formantFilterBP`--------------
Formant filter based on a single resonant bandpass filter.
Formant parameters are linearly interpolated allowing to go smoothly from
one vowel to another. Voice type can be selected but must correspond to
the frequency range of the provided source to be realistic.
#### Usage
```faust
_ : formantFilterBP(voiceType,vowel,nFormants,i,freq) : _
```
Where:
* `voiceType`: the voice type (0: alto, 1: bass, 2: countertenor, 3: soprano, 4: tenor)
* `vowel`: the vowel (0: a, 1: e, 2: i, 3: o, 4: u)
* `nFormants`: number of formant regions in frequency domain, typically 5
* `i`: formant index used to index formant data value arrays
* `freq`: fundamental frequency of excitation signal.
#### Test
```faust
pm = library("physmodels.lib");
formantFilterBP_test = pm.formantFilterBP(0, 0, 5, 0, 200);
```

---

## pm.formantFilterbank

-------`(pm.)formantFilterbank`--------------
Formant filterbank which can use different types of filterbank
functions and different excitation signals. Formant parameters are
linearly interpolated allowing to go smoothly from one vowel to another.
Voice type can be selected but must correspond to the frequency range
of the provided source to be realistic.
#### Usage
```faust
_ : formantFilterbank(voiceType,vowel,formantGen,freq) : _
```
Where:
* `voiceType`: the voice type (0: alto, 1: bass, 2: countertenor, 3: soprano, 4: tenor)
* `vowel`: the vowel (0: a, 1: e, 2: i, 3: o, 4: u)
* `formantGen`: the specific formant filterbank function
(i.e. FormantFilterbankBP, FormantFilterbankFof,...)
* `freq`: fundamental frequency of excitation signal. Needed for FOF
version to calculate rise time of envelope
#### Test
```faust
pm = library("physmodels.lib");
formantFilterbank_test = pm.formantFilterbank(0, 0, 5, 0);
```

---

## pm.formantFilterbankFofCycle

-----`(pm.)formantFilterbankFofCycle`-----
Formant filterbank based on a bank of fof filters.
Formant parameters are linearly interpolated allowing to go smoothly from
one vowel to another. Voice type can be selected but must correspond to
the frequency range of the provided source to be realistic.
#### Usage
```faust
_ : formantFilterbankFofCycle(voiceType,vowel,freq) : _
```
Where:
* `voiceType`: the voice type (0: alto, 1: bass, 2: countertenor, 3: soprano, 4: tenor)
* `vowel`: the vowel (0: a, 1: e, 2: i, 3: o, 4: u)
* `freq`: the fundamental frequency of the excitation signal. Needed to calculate the skirtwidth
of the FOF envelopes and for the autobendFreq and vocalEffort functions
#### Test
```faust
pm = library("physmodels.lib");
formantFilterbankFofCycle_test = pm.formantFilterbankFofCycle(0, 0, 5));
```

---

## pm.formantFilterbankFofSmooth

-----`(pm.)formantFilterbankFofSmooth`----
Formant filterbank based on a bank of fof filters.
Formant parameters are linearly interpolated allowing to go smoothly from
one vowel to another. Voice type can be selected but must correspond to
the frequency range of the provided source to be realistic.
#### Usage
```faust
_ : formantFilterbankFofSmooth(voiceType,vowel,freq) : _
```
Where:
* `voiceType`: the voice type (0: alto, 1: bass, 2: countertenor, 3: soprano, 4: tenor)
* `vowel`: the vowel (0: a, 1: e, 2: i, 3: o, 4: u)
* `freq`: the fundamental frequency of the excitation signal. Needed to
calculate the skirtwidth of the FOF envelopes and for the
autobendFreq and vocalEffort functions
#### Test
```faust
pm = library("physmodels.lib");
formantFilterbankFofSmooth_test = pm.formantFilterbankFofSmooth(0, 0, 5);
```

---

## pm.formantFilterbankBP

-------`(pm.)formantFilterbankBP`--------------
Formant filterbank based on a bank of resonant bandpass filters.
Formant parameters are linearly interpolated allowing to go smoothly from
one vowel to another. Voice type can be selected but must correspond to
the frequency range of the provided source to be realistic.
#### Usage
```faust
_ : formantFilterbankBP(voiceType,vowel,freq) : _
```
Where:
* `voiceType`: the voice type (0: alto, 1: bass, 2: countertenor, 3: soprano, 4: tenor)
* `vowel`: the vowel (0: a, 1: e, 2: i, 3: o, 4: u)
* `freq`: the fundamental frequency of the excitation signal. Needed for the autobendFreq and vocalEffort functions.
#### Test
```faust
pm = library("physmodels.lib");
formantFilterbankBP_test = pm.formantFilterbankBP(0, 0, 5);
```

---

## pm.SFFormantModel

-------`(pm.)SFFormantModel`--------------
Simple formant/vocal synthesizer based on a source/filter model. The `source`
and `filterbank` must be specified by the user. `filterbank` must take the same
input parameters as [`formantFilterbank`](#formantFilterbank) (`BP`/`FofCycle`
/`FofSmooth`).
Formant parameters are linearly interpolated allowing to go smoothly from
one vowel to another. Voice type can be selected but must correspond to
the frequency range of the synthesized voice to be realistic.
#### Usage
```faust
SFFormantModel(voiceType,vowel,exType,freq,gain,source,filterbank,isFof) : _
```
Where:
* `voiceType`: the voice type (0: alto, 1: bass, 2: countertenor, 3: soprano, 4: tenor)
* `vowel`: the vowel (0: a, 1: e, 2: i, 3: o, 4: u
* `exType`: voice vs. fricative sound ratio (0-1 where 1 is 100% fricative)
* `freq`: the fundamental frequency of the source signal
* `gain`: linear gain multiplier to multiply the source by
* `isFof`: whether model is FOF based (0: no, 1: yes)
#### Test
```faust
pm = library("physmodels.lib");
SFFormantModel_test = pm.SFFormantModel(0, 0, 0.5, 0.6, 100, 2, 1, 1);
```

---

## pm.SFFormantModelFofCycle

-------`(pm.)SFFormantModelFofCycle`-------
Simple formant/vocal synthesizer based on a source/filter model. The source
is just a periodic impulse and the "filter" is a bank of FOF filters.
Formant parameters are linearly interpolated allowing to go smoothly from
one vowel to another. Voice type can be selected but must correspond to
the frequency range of the synthesized voice to be realistic. This model
does not work with noise in the source signal so exType has been removed
and model does not depend on SFFormantModel function.
#### Usage
```faust
SFFormantModelFofCycle(voiceType,vowel,freq,gain) : _
```
Where:
* `voiceType`: the voice type (0: alto, 1: bass, 2: countertenor, 3: soprano, 4: tenor)
* `vowel`: the vowel (0: a, 1: e, 2: i, 3: o, 4: u
* `freq`: the fundamental frequency of the source signal
* `gain`: linear gain multiplier to multiply the source by
#### Test
```faust
pm = library("physmodels.lib");
SFFormantModelFofCycle_test = pm.SFFormantModelFofCycle(0.5, 0.6, 0.7);
```

---

## pm.SFFormantModelFofSmooth

-------`(pm.)SFFormantModelFofSmooth`-------
Simple formant/vocal synthesizer based on a source/filter model. The source
is just a periodic impulse and the "filter" is a bank of FOF filters.
Formant parameters are linearly interpolated allowing to go smoothly from
one vowel to another. Voice type can be selected but must correspond to
the frequency range of the synthesized voice to be realistic.
#### Usage
```faust
SFFormantModelFofSmooth(voiceType,vowel,freq,gain) : _
```
Where:
* `voiceType`: the voice type (0: alto, 1: bass, 2: countertenor, 3: soprano, 4: tenor)
* `vowel`: the vowel (0: a, 1: e, 2: i, 3: o, 4: u
* `freq`: the fundamental frequency of the source signal
* `gain`: linear gain multiplier to multiply the source by
#### Test
```faust
pm = library("physmodels.lib");
SFFormantModelFofSmooth_test = pm.SFFormantModelFofSmooth(0.5, 0.6, 0.7);
```

---

## pm.SFFormantModelBP

-------`(pm.)SFFormantModelBP`--------------
Simple formant/vocal synthesizer based on a source/filter model. The source
is just a sawtooth wave and the "filter" is a bank of resonant bandpass filters.
Formant parameters are linearly interpolated allowing to go smoothly from
one vowel to another. Voice type can be selected but must correspond to
the frequency range of the synthesized voice to be realistic.
The formant data used here come from the CSOUND manual
<http://www.csounds.com/manual/html/>.
#### Usage
```faust
SFFormantModelBP(voiceType,vowel,exType,freq,gain) : _
```
Where:
* `voiceType`: the voice type (0: alto, 1: bass, 2: countertenor, 3: soprano, 4: tenor)
* `vowel`: the vowel (0: a, 1: e, 2: i, 3: o, 4: u
* `exType`: voice vs. fricative sound ratio (0-1 where 1 is 100% fricative)
* `freq`: the fundamental frequency of the source signal
* `gain`: linear gain multiplier to multiply the source by
#### Test
```faust
pm = library("physmodels.lib");
SFFormantModelBP_test = pm.SFFormantModelBP(0.5, 0.6, 0.7);
```

---

## pm.SFFormantModelFofCycle_ui

-------`(pm.)SFFormantModelFofCycle_ui`----------
Ready-to-use source-filter vocal synthesizer with built-in user interface.
#### Usage
```faust
SFFormantModelFofCycle_ui : _
```
#### Test
```faust
pm = library("physmodels.lib");
SFFormantModelFofCycle_ui_test = pm.SFFormantModelFofCycle_ui;
```

---

## pm.SFFormantModelFofSmooth_ui

-------`(pm.)SFFormantModelFofSmooth_ui`----------
Ready-to-use source-filter vocal synthesizer with built-in user interface.
#### Usage
```faust
SFFormantModelFofSmooth_ui : _
```
#### Test
```faust
pm = library("physmodels.lib");
SFFormantModelFofSmooth_ui_test = pm.SFFormantModelFofSmooth_ui;
```

---

## pm.SFFormantModelBP_ui

-------`(pm.)SFFormantModelBP_ui`----------
Ready-to-use source-filter vocal synthesizer with built-in user interface.
#### Usage
```faust
SFFormantModelBP_ui : _
```
#### Test
```faust
pm = library("physmodels.lib");
SFFormantModelBP_ui_test = pm.SFFormantModelBP_ui;
```

---

## pm.SFFormantModelFofCycle_ui_MIDI

-------`(pm.)SFFormantModelFofCycle_ui_MIDI`----------
Ready-to-use MIDI-controllable source-filter vocal synthesizer.
#### Usage
```faust
SFFormantModelFofCycle_ui_MIDI : _
```
#### Test
```faust
pm = library("physmodels.lib");
SFFormantModelFofCycle_ui_MIDI_test = pm.SFFormantModelFofCycle_ui_MIDI;
```

---

## pm.SFFormantModelFofSmooth_ui_MIDI

-------`(pm.)SFFormantModelFofSmooth_ui_MIDI`----------
Ready-to-use MIDI-controllable source-filter vocal synthesizer.
#### Usage
```faust
SFFormantModelFofSmooth_ui_MIDI : _
```
#### Test
```faust
pm = library("physmodels.lib");
SFFormantModelFofSmooth_ui_MIDI_test = pm.SFFormantModelFofSmooth_ui_MIDI;
```

---

## pm.SFFormantModelBP_ui_MIDI

-------`(pm.)SFFormantModelBP_ui_MIDI`----------
Ready-to-use MIDI-controllable source-filter vocal synthesizer.
#### Usage
```faust
SFFormantModelBP_ui_MIDI : _
```
#### Test
```faust
pm = library("physmodels.lib");
SFFormantModelBP_ui_MIDI_test = pm.SFFormantModelBP_ui_MIDI;
```

---

## pm.allpassNL

-------`(pm.)allpassNL`--------------
Bidirectional block adding nonlinearities in both directions in a chain.
Nonlinearities are created by modulating the coefficients of a passive
allpass filter by the signal it is processing.
#### Usage
```faust
chain(... : allpassNL(nonlinearity) : ...)
```
Where:
* `nonlinearity`: amount of nonlinearity to be added (0-1)
#### Test
```faust
pm = library("physmodels.lib");
allpassNL_test = 0,0,0 : pm.allpassNL(0.4);
```

---

## pm.modalModel

-------`(pm.)modalModel`--------------
Implement multiple resonance modes using resonant bandpass filters.
#### Usage
```faust
_ : modalModel(n, freqs, t60s, gains) : _
```
Where:
* `n`: number of given modes
* `freqs` : list of filter center freqencies
* `t60s` : list of mode resonance durations (in seconds)
* `gains` : list of mode gains (0-1)
For example, to generate a model with 2 modes (440 Hz and 660 Hz, a
fifth) where the higher one decays faster and is attenuated:
```faust
os.impulse : modalModel(2, (440, 660),
(0.5, 0.25),
(ba.db2linear(-1), ba.db2linear(-6)) : _
```
#### Test
```faust
pm = library("physmodels.lib");
os = library("oscillators.lib");
modalModel_test = os.impulse : pm.modalModel(3, (440,660,880), (0.5,0.4,0.3), (0.8,0.6,0.4));
```
Further reading: [Grumiaux et. al., 2017:
Impulse-Response and CAD-Model-Based Physical Modeling in
Faust](https://raw.githubusercontent.com/grame-cncm/faust/master-dev/tools/physicalModeling/ir2dsp/lacPaper2017.pdf)

---

## pm.rk_solve

-----------------------------`(pm.)rk_solve`----------------------------
Solves the system of ordinary differential equations of any order using
the explicit Runge-Kutta methods.
#### Usage
```faust
rk_solve(ts,ks, ni,h, eq,iv) : si.bus(outputs(eq))
```
Where:
* `ts,ks` : the Butcher tableau (see below)
* `ni` : number of iterations at each tick, compile time constant
ni > 1 can improve accuracy but will degrade performance
* `h`  : time step, run time constant, e.g. 1/ma.SR
* `eq` : list of derivative functions
* `iv` : list of initial values
`rk_solve()` with the "standard" 1-4 tableaux and ni = 1:
```faust
rk_solve_1 = rk_solve((0), (1), 1);
rk_solve_2 = rk_solve((0,1/2), (1/2, 0,1), 1);
rk_solve_3 = rk_solve((0,1/2,1), (1/2,-1,2, 1/6,2/3,1/6), 1);
rk_solve_4 = rk_solve((0,1/2,1/2,1), (1/2,0,1/2,0,0,1, 1/6,1/3,1/3,1/6), 1);
```
#### Test
```faust
pm = library("physmodels.lib");
ma = library("maths.lib");
rk_solve_test = pm.rk_solve((0), (1), 1, 1.0/ma.SR, eq, (1)) with { eq(t,x) = -x; };
```
#### Example test program
Suppose we have a system of differential equations:
```faust
dx/dt = dx_dt(t,x,y,z)
dy/dt = dy_dt(t,x,y,z)
dz/dt = dz_dt(t,x,y,z)
```
with initial conditions:
```faust
x(0) = x0
y(0) = y0
z(0) = z0
```
and we want to solve it using this Butcher tableau:
```faust
0 |
c2 | a21
c3 | a31 a32
c4 | a41 a42 a43
-------------------
| b1  b1  b3  b4
```
```faust
EQ(t,x,y,z) = dx_dt(t,x,y,z),
dy_dt(t,x,y,z),
dz_dt(t,x,y,z);

IV = x0, y0, z0;

TS = 0, c2, c3, c4;
KS = a21,
a31, a32,
a41, a42, a43,
b1,  b2,  b3,  b4;

process = rk_solve(TS,KS, 1,1/ma.SR, EQ,IV);
```
Less abstract example which can actually be compiled/tested:
```faust
Lotka-Volterra equations parameterized by a,b,c,d:
LV(a,b,c,d, t,x,y) =
a*x - b*x*y,
c*x*y - d*y;

Solved using the "standard" fourth-order method:
process = rk_solve_4(
0.01,                  // time step
LV(0.1,0.02,0.03,0.4), // LV() with random parameters
(3,4)                  // initial values
);
```
#### References
* <https://wikipedia.org/wiki/Runge%E2%80%93Kutta_methods>

---

# platform.lib
**Prefix:** `pl`

#################################### platform.lib ########################################
A library to handle platform specific code in Faust. Its official prefix is `pl`.

#### References

* <https://github.com/grame-cncm/faustlibraries/blob/master/platform.lib>
########################################################################################
It can be reimplemented to globally change the SR and the tablesize definitions

## pl.SR

---------------------------------`(pl.)SR`-----------------------------------
Current sampling rate (between 1 and 192000Hz). Constant during
program execution. Setting this value to a constant will allow the
compiler to optimize the code by computing constant expressions at
compile time, and can be valuable for performance, especially on
embedded systems.

---

## pl.BS

---------------------------------`(pl.)BS`---------------------------------------
Current block-size (between 1 and 16384 frames). Can change during the execution.

---

## pl.tablesize

---------------------------------`(pl.)tablesize`----------------------------
Oscillator table size. This value is used to define the size of the
table used by the oscillators. It is usually a power of 2 and can be lowered
to save memory. The default value is 65536.

---

# quantizers.lib
**Prefix:** `qu`

################################ quantizers.lib ##########################################
Quantizers library. Its official prefix is `qu`.

This library provides utilities for pitch and signal quantization in Faust.
It includes functions for mapping continuous inputs to discrete musical scales.

The Quantizers library is organized into 1 section:

* [Functions Reference](#functions-reference)

#### References

* <https://github.com/grame-cncm/faustlibraries/blob/master/quantizers.lib>
########################################################################################

## qu.quantize

-------`(qu.)quantize`----------
Configurable frequency quantization tool. Snaps input frequencies to exact scale notes.
Works for positive audio frequencies.
#### Usage
```faust
_ : quantize(rf,nl) : _
```
Where:
* `rf` : frequency of the root note of the scale
* `nl` : list of frequency ratios for each note relative to root
#### Test
```faust
qu = library("quantizers.lib");
quantize_test = qu.quantize(440, qu.ionian, hslider("input", 450, 100, 1000, 1));
```
#### Example
```faust
process = quantize(440, (1, 1.125, 1.25, 1.333, 1.5));
```

---

## qu.quantizeSmoothed

-------`(qu.)quantizeSmoothed`----------
Configurable frequency quantization tool. Smoothly transitions between scale notes.
Works for positive audio frequencies.
#### Usage
```faust
_ : quantizeSmoothed(rf,nl) : _
```
Where:
* `rf` : frequency of the root note of the scale
* `nl` : list of frequency ratios for each note relative to root
#### Test
```faust
qu = library("quantizers.lib");
quantizeSmoothed_test = qu.quantizeSmoothed(440, qu.ionian, hslider("input", 450, 100, 1000, 1));
```
#### Example
```faust
process = quantizeSmoothed(440, dodeca);
```

---

## qu.ionian

---------------------`(qu.)ionian`--------------------------
List of the frequency ratios of the notes of the ionian mode.
#### Usage
```faust
_ : quantize(rf,ionian) : _
```
Where:
* `rf`: frequency of the root note of the scale
#### Test
```faust
qu = library("quantizers.lib");
ionian_test = qu.quantize(220, qu.ionian, 260);
```

---

## qu.dorian

---------------------`(qu.)dorian`--------------------------
List of the frequency ratios of the notes of the dorian mode.
#### Usage
```faust
_ : quantize(rf,dorian) : _
```
Where:
* `rf`: frequency of the root note of the scale
#### Test
```faust
qu = library("quantizers.lib");
dorian_test = qu.quantize(220, qu.dorian, 260);
```

---

## qu.phrygian

---------------------`(qu.)phrygian`--------------------------
List of the frequency ratios of the notes of the phrygian mode.
#### Usage
```faust
_ : quantize(rf,phrygian) : _
```
Where:
* `rf`: frequency of the root note of the scale
#### Test
```faust
qu = library("quantizers.lib");
phrygian_test = qu.quantize(220, qu.phrygian, 260);
```

---

## qu.lydian

---------------------`(qu.)lydian`--------------------------
List of the frequency ratios of the notes of the lydian mode.
#### Usage
```faust
_ : quantize(rf,lydian) : _
```
Where:
* `rf`: frequency of the root note of the scale
#### Test
```faust
qu = library("quantizers.lib");
lydian_test = qu.quantize(220, qu.lydian, 260);
```

---

## qu.mixo

---------------------`(qu.)mixo`--------------------------
List of the frequency ratios of the notes of the mixolydian mode.
#### Usage
```faust
_ : quantize(rf,mixo) : _
```
Where:
* `rf`: frequency of the root note of the scale
#### Test
```faust
qu = library("quantizers.lib");
mixo_test = qu.quantize(220, qu.mixo, 260);
```

---

## qu.eolian

---------------------`(qu.)eolian`--------------------------
List of the frequency ratios of the notes of the eolian mode.
#### Usage
```faust
_ : quantize(rf,eolian) : _
```
Where:
* `rf`: frequency of the root note of the scale
#### Test
```faust
qu = library("quantizers.lib");
eolian_test = qu.quantize(220, qu.eolian, 260);
```

---

## qu.locrian

---------------------`(qu.)locrian`--------------------------
List of the frequency ratios of the notes of the locrian mode.
#### Usage
```faust
_ : quantize(rf,locrian) : _
```
Where:
* `rf`: frequency of the root note of the scale
#### Test
```faust
qu = library("quantizers.lib");
locrian_test = qu.quantize(220, qu.locrian, 260);
```

---

## qu.pentanat

---------------------`(qu.)pentanat`--------------------------
List of the frequency ratios of the notes of the pythagorean tuning for the minor pentatonic scale.
#### Usage
```faust
_ : quantize(rf,pentanat) : _
```
Where:
* `rf`: frequency of the root note of the scale
#### Test
```faust
qu = library("quantizers.lib");
pentanat_test = qu.quantize(220, qu.pentanat, 260);
```

---

## qu.kumoi

---------------------`(qu.)kumoi`--------------------------
List of the frequency ratios of the notes of the kumoijoshi, the japanese pentatonic scale.
#### Usage
```faust
_ : quantize(rf,kumoi) : _
```
Where:
* `rf`: frequency of the root note of the scale
#### Test
```faust
qu = library("quantizers.lib");
kumoi_test = qu.quantize(220, qu.kumoi, 260);
```

---

## qu.natural

---------------------`(qu.)natural`--------------------------
List of the frequency ratios of the notes of the natural major scale.
#### Usage
```faust
_ : quantize(rf,natural) : _
```
Where:
* `rf`: frequency of the root note of the scale
#### Test
```faust
qu = library("quantizers.lib");
natural_test = qu.quantize(220, qu.natural, 260);
```

---

## qu.dodeca

---------------------`(qu.)dodeca`--------------------------
List of the frequency ratios of the notes of the dodecaphonic scale.
#### Usage
```faust
_ : quantize(rf,dodeca) : _
```
Where:
* `rf`: frequency of the root note of the scale
#### Test
```faust
qu = library("quantizers.lib");
dodeca_test = qu.quantize(220, qu.dodeca, 260);
```

---

## qu.dimin

---------------------`(qu.)dimin`--------------------------
List of the frequency ratios of the notes of the diminished scale.
#### Usage
```faust
_ : quantize(rf,dimin) : _
```
Where:
* `rf`: frequency of the root note of the scale
#### Test
```faust
qu = library("quantizers.lib");
dimin_test = qu.quantize(220, qu.dimin, 260);
```

---

## qu.penta

---------------------`(qu.)penta`--------------------------
List of the frequency ratios of the notes of the minor pentatonic scale.
#### Usage
```faust
_ : quantize(rf,penta) : _
```
Where:
* `rf`: frequency of the root note of the scale
#### Test
```faust
qu = library("quantizers.lib");
penta_test = qu.quantize(220, qu.penta, 260);
```

---

# reducemaps.lib
**Prefix:** `re`

############################# reducemaps.lib ###############################
A library providing reduce/map operations in Faust. Its official prefix is
`rm`.

The basic idea behind _reduce_ operations is to combine several values
into a single one by repeatedly applying a binary operation. A typical
example is finding the maximum of a set of values by repeatedly applying the
binary operation `max`.

In this reducemaps library, you'll find two types of _reduce_, depending on
whether you want to reduce n consecutive samples of the same signal or a set
of n parallel signals.

#### References

* <https://github.com/grame-cncm/faustlibraries/blob/master/reducemaps.lib>
#############################################################################

## rm.parReduce

----------------------------`(rm.)parReduce`--------------------------------
`parReduce(op,N)` combines a set of `N` parallel signals into a single one
using a binary operation `op`.
With `parReduce`, this reduction process simultaneously occurs on each half
of the incoming signals. In other words, `parReduce(max,256)` is equivalent
to `parReduce(max,128),parReduce(max,128) : max`.
To be used with `parReduce`, binary operation `op` must be associative.
Additionally, the concept of a binary operation extends to operations
that have `2*n` inputs and `n` outputs. For example, complex signals can be
simulated using two signals for the real and imaginary parts. In
such case, a binary operation would have 4 inputs and 2 outputs.
Please note also that `parReduce` is faster than `topReduce` or `botReduce`
for large number of signals. It is therefore the recommended operation
whenever `op` is associative.
#### Usage
```faust
_,...,_ : parReduce(op, N) : _
```
Where:
* `op`: is a binary operation
* `N`: is the number of incomming signals (`N>0`). We use a capital letter
here to indicate that the number of incomming signals must be constant and
known at compile time.
#### Test
```faust
rm = library("reducemaps.lib");
parReduce_test = (1,2,3,4) : rm.parReduce(+, 4);
```

---

## rm.topReduce

----------------------------`(rm.)topReduce`--------------------------------
`topReduce(op,N)` involves combining a set of `N` parallel signals into a
single one using a binary operation `op`. With `topReduce`, the reduction
process starts from the top two incoming signals, down to the bottom. In
other words, `topReduce(max,256)` is equivalent to `topReduce(max,255),_ : max`.
Contrary to `parReduce`, the binary operation `op` doesn't have to be
associative here. Like with `parReduce` the concept of a binary operation can be
extended to operations that have 2*n inputs and n outputs. For example,
complex signals can be simulated using two signals representing the real and
imaginary parts. In such cases, a binary operation would have 4 inputs and 2
outputs.
#### Usage
```faust
_,...,_ : topReduce(op, N) : _
```
Where:
* `op`: is a binary operation
* `N`: is the number of incomming signals (`N>0`). We use a capital letter
here to indicate that the number of incomming signals must be constant and
known at compile time.
#### Test
```faust
rm = library("reducemaps.lib");
topReduce_test = (1,2,3,4) : rm.topReduce(+, 4);
```

---

## rm.botReduce

----------------------------`(rm.)botReduce`--------------------------------
`botReduce(op,N)` combines a set of `N` parallel signals into a single one
using a binary operation `op`. With `botReduce`, the reduction process starts
from the bottom two incoming signals, up to the top. In other words,
`botReduce(max,256)` is equivalent to `_,botReduce(max,255): max`.
Contrary to `parReduce`, the binary operation `op` doesn't have to be
associative here. Like with `parReduce` the concept of a binary operation can be
extended to operations that have 2*n inputs and n outputs. For example,
complex signals can be simulated using two signals representing the real and
imaginary parts. In such cases, a binary operation would have 4 inputs and 2
outputs.
#### Usage
```faust
_,...,_ : botReduce(op, N) : _
```
Where:
* op: is a binary operation
* N: is the number of incomming signals (`N>0`). We use a capital letter
here to indicate that the number of incomming signals must be constant and
known at compile time.
#### Test
```faust
rm = library("reducemaps.lib");
botReduce_test = (1,2,3,4) : rm.botReduce(+, 4);
```

---

## rm.reduce

--------------------------------`(rm.)reduce`--------------------------------
Reduce a block of `n` consecutive samples of the incomming signal using a
binary operation `op`. For example: `reduce(max,128)` will compute the
maximun value of each block of 128 samples. Please note that the resulting
value, while computed continuously, will be constant for the duration of a
block. A new value is only produced at the end of a block. Note also that
blocks should be of at least one sample (n>0).
#### Usage
```faust
_ : reduce(op, n) : _
```
Where:
* `op`: is a binary operation
* `n`: is the number of consecutive samples in a block.
#### Test
```faust
rm = library("reducemaps.lib");
reduce_test = rm.reduce(max, 4, hslider("reduce:input", 0, -1, 1, 0.01));
```

---

## rm.reducemap

--------------------`(rm.)reducemap`---------------------------
Like `reduce` but a `foo` function is applied to the result. From
a mathematical point of view:
`reducemap(op,foo,n)` is equivalent to `reduce(op,n):foo`
but more efficient.
#### Usage
```faust
_ : reducemap(op, foo, n) : _
```
Where:
* `op`: is a binary operation
* `foo`: is a function applied to the result of the reduction
* `n`: is the number of consecutive samples in a block.
#### Test
```faust
rm = library("reducemaps.lib");
reducemap_test = rm.reducemap(+, /(4), 4, hslider("reducemap:input", 0, -1, 1, 0.01));
```

---

# reverbs.lib
**Prefix:** `re`

################################ reverbs.lib ##########################################
Reverbs library. Its official prefix is `re`.

This library provides a collection of artificial reverberation algorithms in Faust.
It includes Schroeder, Moorer, Freeverb, and FDN-based designs. These modules can be used
for room simulation, spatialization, and creative ambience design in both mono and multichannel contexts.

The Reverbs library is organized into 7 sections:

* [Schroeder Reverberators](#schroeder-reverberators)
* [Feedback Delay Network (FDN) Reverberators](#feedback-delay-network-fdn-reverberators)
* [Freeverb](#freeverb)
* [Dattorro Reverb](#dattorro-reverb)
* [JPverb and Greyhole Reverbs](#jpverb-and-greyhole-reverbs)
* [Keith Barr Allpass Loop Reverb](#keith-barr-allpass-loop-reverb)
* [Others](#respringreverb)
#### References

* <https://github.com/grame-cncm/faustlibraries/blob/master/reverbs.lib>
########################################################################################

## re.jcrev

------------------------------`(re.)jcrev`------------------------------
This artificial reverberator take a mono signal and output stereo
(`satrev`) and quad (`jcrev`). They were implemented by John Chowning
in the MUS10 computer-music language (descended from Music V by Max
Mathews).  They are Schroeder Reverberators, well tuned for their size.
Nowadays, the more expensive freeverb is more commonly used (see the
Faust examples directory).
`jcrev` reverb below was made from a listing of "RV", dated April 14, 1972,
which was recovered from an old SAIL DART backup tape.
John Chowning thinks this might be the one that became the
well known and often copied JCREV.
`jcrev` is a standard Faust function.
#### Usage
```faust
_ : jcrev : _,_,_,_
```
#### Test
```faust
re = library("reverbs.lib");
os = library("oscillators.lib");
jcrev_test = os.osc(440) : re.jcrev;
```

---

## re.satrev

------------------------------`(re.)satrev`------------------------------
This artificial reverberator take a mono signal and output stereo
(`satrev`) and quad (`jcrev`).  They were implemented by John Chowning
in the MUS10 computer-music language (descended from Music V by Max
Mathews).  They are Schroeder Reverberators, well tuned for their size.
Nowadays, the more expensive freeverb is more commonly used (see the
Faust examples directory).
`satrev` was made from a listing of "SATREV", dated May 15, 1971,
which was recovered from an old SAIL DART backup tape.
John Chowning thinks this might be the one used on his
often-heard brass canon sound examples, one of which can be found at
<https://ccrma.stanford.edu/~jos/wav/FM-BrassCanon2.wav>.
#### Usage
```faust
_ : satrev : _,_
```
#### Test
```faust
re = library("reverbs.lib");
os = library("oscillators.lib");
satrev_test = os.osc(330) : re.satrev;
```

---

## re.fdnrev0

--------------------------------`(re.)fdnrev0`---------------------------------
Pure Feedback Delay Network Reverberator (generalized for easy scaling).
`fdnrev0` is a standard Faust function.
#### Usage
```faust
<1,2,4,...,N signals> <:
fdnrev0(MAXDELAY,delays,BBSO,freqs,durs,loopgainmax,nonl) :>
<1,2,4,...,N signals>
```
Where:
* `N`: 2, 4, 8, ...  (power of 2)
* `MAXDELAY`: power of 2 at least as large as longest delay-line length
* `delays`: N delay lines, N a power of 2, lengths preferably coprime
* `BBSO`: odd positive integer = order of bandsplit desired at freqs
* `freqs`: NB-1 crossover frequencies separating desired frequency bands
* `durs`: NB decay times (t60) desired for the various bands
* `loopgainmax`: scalar gain between 0 and 1 used to "squelch" the reverb
* `nonl`: nonlinearity (0 to 0.999..., 0 being linear)
#### Test
```faust
re = library("reverbs.lib");
os = library("oscillators.lib");
fdnrev0_test = (os.osc(220), os.osc(330), os.osc(440), os.osc(550))
<: re.fdnrev0(4096, (149, 211, 263, 293), 1, (800, 4000), (2.5, 2.0, 1.5), 0.8, 0.0);
```
#### References
* <https://ccrma.stanford.edu/~jos/pasp/FDN_Reverberation.html>

---

## re.zita_rev_fdn

-------------------------------`(re.)zita_rev_fdn`-------------------------------
Internal 8x8 late-reverberation FDN used in the FOSS Linux reverb `zita-rev1`
by Fons Adriaensen <fons@linuxaudio.org>.  This is an FDN reverb with
allpass comb filters in each feedback delay in addition to the
damping filters.
#### Usage
```faust
si.bus(8) : zita_rev_fdn(f1,f2,t60dc,t60m,fsmax) : si.bus(8)
```
Where:
* `f1`: crossover frequency (Hz) separating dc and midrange frequencies
* `f2`: frequency (Hz) above f1 where T60 = t60m/2 (see below)
* `t60dc`: desired decay time (t60) at frequency 0 (sec)
* `t60m`: desired decay time (t60) at midrange frequencies (sec)
* `fsmax`: maximum sampling rate to be used (Hz)
#### Test
```faust
re = library("reverbs.lib");
os = library("oscillators.lib");
zita_rev_fdn_test = par(i, 8, os.osc(110 * (i + 1)))
<: re.zita_rev_fdn(200, 2000, 3.0, 2.0, 48000);
```
#### References
* <http://www.kokkinizita.net/linuxaudio/zita-rev1-doc/quickguide.html>
* <https://ccrma.stanford.edu/~jos/pasp/Zita_Rev1.html>

---

## re.zita_rev1_stereo

----------------------------`(re.)zita_rev1_stereo`---------------------------
Extend `zita_rev_fdn` to include `zita_rev1` input/output mapping in stereo mode.
`zita_rev1_stereo` is a standard Faust function.
#### Usage
```faust
_,_ : zita_rev1_stereo(rdel,f1,f2,t60dc,t60m,fsmax) : _,_
```
Where:
`rdel`  = delay (in ms) before reverberation begins (e.g., 0 to ~100 ms)
(remaining args and refs as for `zita_rev_fdn` above)
#### Test
```faust
re = library("reverbs.lib");
os = library("oscillators.lib");
zita_rev1_stereo_test = (os.osc(440), os.osc(550))
: re.zita_rev1_stereo(20, 200, 2000, 3.0, 2.0, 48000);
```

---

## re.zita_rev1_ambi

-----------------------------`(re.)zita_rev1_ambi`---------------------------
Extend `zita_rev_fdn` to include `zita_rev1` input/output mapping in
"ambisonics mode", as provided in the Linux C++ version.
#### Usage
```faust
_,_ : zita_rev1_ambi(rgxyz,rdel,f1,f2,t60dc,t60m,fsmax) : _,_,_,_
```
Where:
`rgxyz` = relative gain of lanes 1,4,2 to lane 0 in output (e.g., -9 to 9)
(remaining args and references as for zita_rev1_stereo above)
#### Test
```faust
re = library("reverbs.lib");
os = library("oscillators.lib");
zita_rev1_ambi_test = (os.osc(330), os.osc(550))
: re.zita_rev1_ambi(0.0, 25, 200, 2000, 3.0, 2.0, 48000);
```

---

## re.vital_rev

-------------------`(re.)vital_rev`------------------------------------------
A port of the reverb from the Vital synthesizer. All input parameters
have been normalized to a continuous [0,1] range, making them easy to modulate.
The scaling of the parameters happens inside the function.
#### Usage
```faust
_,_ : vital_rev(prelow, prehigh, lowcutoff, highcutoff, lowgain, highgain, chorus_amt, chorus_freq, predelay, time, size, mix) : _,_ 
```
Where:
* `prelow`: In the pre-filter, this is the cutoff frequency of a high-pass filter (hence a low value)
* `prehigh`: In the pre-filter, this is the cutoff frequency of a low-pass filter (hence a high value)
* `lowcutoff`: In the feedback filter stage, this is the cutoff frequency of a low-shelf filter
* `highcutoff`: In the feedback filter stage, this is the cutoff frequency of a high-shelf filter
* `lowgain`: In the feedback filter stage, this is the gain of a low-shelf filter
* `highgain`: In the feedback filter stage, this is the gain of a high-shelf filter
* `chorus_amt`: The amount of chorus modulation in the main delay lines
* `chorus_freq`: The LFO rate of chorus modulation in the main delay lines
* `predelay`: The amount of pre-delay time
* `time`: The decay time of the reverb
* `size`: The size of the room
* `mix`: A wetness value to use in a final dry/wet mixer
#### Test
```faust
re = library("reverbs.lib");
os = library("oscillators.lib");
vital_rev_test = (os.osc(330), os.osc(440))
: re.vital_rev(0.2, 0.8, 0.5, 0.7, 0.4, 0.6, 0.3, 0.2, 0.1, 0.7, 0.5, 0.4);
```

---

## re.mono_freeverb

----------------------------`(re.)mono_freeverb`-------------------------
A simple Schroeder reverberator primarily developed by "Jezar at Dreampoint" that
is extensively used in the free-software world. It uses four Schroeder allpasses in
series and eight parallel Schroeder-Moorer filtered-feedback comb-filters for each
audio channel, and is said to be especially well tuned.
`mono_freeverb` is a standard Faust function.
#### Usage
```faust
_ : mono_freeverb(fb1, fb2, damp, spread) : _
```
Where:
* `fb1`: coefficient of the lowpass comb filters (0-1)
* `fb2`: coefficient of the allpass comb filters (0-1)
* `damp`: damping of the lowpass comb filter (0-1)
* `spread`: spatial spread in number of samples (for stereo)
#### Test
```faust
re = library("reverbs.lib");
os = library("oscillators.lib");
mono_freeverb_test = os.osc(440) : re.mono_freeverb(0.7, 0.5, 0.3, 30);
```
#### License
While this version is licensed LGPL (with exception) along with other GRAME
library functions, the file freeverb.dsp in the examples directory of older
Faust distributions, such as faust-0.9.85, was released under the BSD license,
which is less restrictive.

---

## re.stereo_freeverb

----------------------------`(re.)stereo_freeverb`-------------------------
A simple Schroeder reverberator primarily developed by "Jezar at Dreampoint" that
is extensively used in the free-software world. It uses four Schroeder allpasses in
series and eight parallel Schroeder-Moorer filtered-feedback comb-filters for each
audio channel, and is said to be especially well tuned.
#### Usage
```faust
_,_ : stereo_freeverb(fb1, fb2, damp, spread) : _,_
```
Where:
* `fb1`: coefficient of the lowpass comb filters (0-1)
* `fb2`: coefficient of the allpass comb filters (0-1)
* `damp`: damping of the lowpass comb filter (0-1)
* `spread`: spatial spread in number of samples (for stereo)
#### Test
```faust
re = library("reverbs.lib");
os = library("oscillators.lib");
stereo_freeverb_test = (os.osc(330), os.osc(550))
: re.stereo_freeverb(0.7, 0.5, 0.3, 30);
```

---

## re.dattorro_rev

-------------------------------`(re.)dattorro_rev`-------------------------------
Reverberator based on the Dattorro reverb topology. This implementation does
not use modulated delay lengths (excursion).
#### Usage
```faust
_,_ : dattorro_rev(pre_delay, bw, i_diff1, i_diff2, decay, d_diff1, d_diff2, damping) : _,_
```
Where:
* `pre_delay`: pre-delay in samples (fixed at compile time)
* `bw`: band-width filter (pre filtering); (0 - 1)
* `i_diff1`: input diffusion factor 1; (0 - 1)
* `i_diff2`: input diffusion factor 2;
* `decay`: decay rate; (0 - 1); infinite decay = 1.0
* `d_diff1`: decay diffusion factor 1; (0 - 1)
* `d_diff2`: decay diffusion factor 2;
* `damping`: high-frequency damping; no damping = 0.0
#### Test
```faust
re = library("reverbs.lib");
os = library("oscillators.lib");
dattorro_rev_test = (os.osc(330), os.osc(550))
: re.dattorro_rev(200, 0.5, 0.7, 0.6, 0.5, 0.7, 0.5, 0.2);
```
#### References
* <https://ccrma.stanford.edu/~dattorro/EffectDesignPart1.pdf>

---

## re.dattorro_rev_default

-------------------------------`(re.)dattorro_rev_default`-------------------------------
Reverberator based on the Dattorro reverb topology with reverb parameters from the
original paper.
This implementation does not use modulated delay lengths (excursion) and
uses zero length pre-delay.
#### Usage
```faust
_,_ : dattorro_rev_default : _,_
```
#### Test
```faust
re = library("reverbs.lib");
os = library("oscillators.lib");
dattorro_rev_default_test = (os.osc(330), os.osc(550))
: re.dattorro_rev_default;
```
#### References
* <https://ccrma.stanford.edu/~dattorro/EffectDesignPart1.pdf>

---

## re.jpverb

-------------------------------`(re.)jpverb`-------------------------------
An algorithmic reverb (stereo in/out), inspired by the lush chorused sound
of certain vintage Lexicon and Alesis reverberation units.
Designed to sound great with synthetic sound sources, rather than sound like a realistic space.
#### Usage
```faust
_,_ : jpverb(t60, damp, size, early_diff, mod_depth, mod_freq, low, mid, high, low_cutoff, high_cutoff) : _,_
```
Where:
* `t60`: approximate reverberation time in seconds ([0.1..60] sec) (T60 - the time for the reverb to decay by 60db when damp == 0 ). Does not effect early reflections
* `damp`: controls damping of high-frequencies as the reverb decays. 0 is no damping, 1 is very strong damping. Values should be in the range ([0..1])
* `size`: scales size of delay-lines within the reverberator, producing the impression of a larger or smaller space. Values below 1 can sound metallic. Values should be in the range [0.5..5]
* `early_diff`: controls shape of early reflections. Values of 0.707 or more produce smooth exponential decay. Lower values produce a slower build-up of echoes. Values should be in the range ([0..1])
* `mod_depth`: depth ([0..1]) of delay-line modulation. Use in combination with `mod_freq` to set amount of chorusing within the structure
* `mod_freq`: frequency ([0..10] Hz) of delay-line modulation. Use in combination with `mod_depth` to set amount of chorusing within the structure
* `low`: multiplier ([0..1]) for the reverberation time within the low band
* `mid`: multiplier ([0..1]) for the reverberation time within the mid band
* `high`: multiplier ([0..1]) for the reverberation time within the high band
* `low_cutoff`: frequency (100..6000 Hz) at which the crossover between the low and mid bands of the reverb occurs
* `high_cutoff`: frequency (1000..10000 Hz) at which the crossover between the mid and high bands of the reverb occurs
#### Test
```faust
re = library("reverbs.lib");
os = library("oscillators.lib");
jpverb_test = (os.osc(330), os.osc(440))
: re.jpverb(3.0, 0.2, 1.0, 0.8, 0.3, 0.4, 0.9, 0.8, 0.7, 500, 4000);
```
#### References
* <https://doc.sccode.org/Overviews/DEIND.html>

---

## re.greyhole

-------------------------------`(re.)greyhole`-------------------------------
A complex echo-like effect (stereo in/out), inspired by the classic Eventide effect of a similar name.
The effect consists of a diffuser (like a mini-reverb, structurally similar to the one used in `jpverb`)
connected in a feedback system with a long, modulated delay-line.
Excels at producing spacey washes of sound.
#### Usage
```faust
_,_ : greyhole(dt, damp, size, early_diff, feedback, mod_depth, mod_freq) : _,_
```
Where:
* `dt`: approximate reverberation time in seconds ([0.1..60 sec])
* `damp`: controls damping of high-frequencies as the reverb decays. 0 is no damping, 1 is very strong damping. Values should be between ([0..1])
* `size`: control of relative "room size" roughly in the range ([0.5..3])
* `early_diff`: controls pattern of echoes produced by the diffuser. At very low values, the diffuser acts like a delay-line whose length is controlled by the 'size' parameter. Medium values produce a slow build-up of echoes, giving the sound a reversed-like quality. Values of 0.707 or greater than produce smooth exponentially decaying echoes. Values should be in the range ([0..1])
* `feedback`: amount of feedback through the system. Sets the number of repeating echoes. A setting of 1.0 produces infinite sustain. Values should be in the range ([0..1])
* `mod_depth`: depth ([0..1]) of delay-line modulation. Use in combination with `mod_freq` to produce chorus and pitch-variations in the echoes
* `mod_freq`: frequency ([0..10] Hz) of delay-line modulation. Use in combination with `mod_depth` to produce chorus and pitch-variations in the echoes
#### Test
```faust
re = library("reverbs.lib");
os = library("oscillators.lib");
greyhole_test = (os.osc(220), os.osc(440))
: re.greyhole(2.0, 0.3, 1.0, 0.6, 0.5, 0.4, 0.2);
```
#### References
* <https://doc.sccode.org/Overviews/DEIND.html>

---

## re.kb_rom_rev1

----------------------------`(re.)kb_rom_rev1`---------------------------
Reverberator based on Keith Barr's all-pass single feedback loop reverb topology. Originally designed for the Spin Semiconductor FV-1 chip, this code is an adaptation of the rom_rev1.spn file, part of the Spin Semiconductor Free DSP Programs available on the Spin Semiconductor website.
It was submitted by Keith Barr himself and written in Spin Semiconductor Assembly, a dedicated assembly language for programming the FV-1 chip.
In this topology, when multiple delays and all-pass filters are placed in a loop, sound injected into the loop will recirculate, increasing the density of any impulse as the signal successively passes through the all-pass filters.
The result, after a short period of time, is a wash of sound, completely diffused into a natural reverb tail.
The reverb typically has a mono input (as from a single source) but benefits from a stereo output, providing the listener with a fuller, more immersive reverberant image.
#### Usage
```faust
_,_ : kb_rom_rev1(rt, damp) : _,_
```
Where:
* `rt`: coefficent of the decay of the reverb (0-1)
* `damp`: coefficient of the lowpass filters (0-1)
#### Test
```faust
re = library("reverbs.lib");
os = library("oscillators.lib");
kb_rom_rev1_test = (os.osc(330), os.osc(660))
: re.kb_rom_rev1(0.7, 0.3);
```
#### References
* <https://www.spinsemi.com/programs.php#:~:text=Keith%20Barr-,rom_rev1.spn,-ROM%20reverb%202>
* <https://www.spinsemi.com/knowledge_base/effects.html#Reverberation>
* <https://www.spinsemi.com/knowledge_base/inst_syntax.html>

---

## re.springreverb

-------------------------------`(re.)springreverb`-------------------------------
Mono spring-inspired reverb originally designed for the Chaos Audio Stratus, which defines all parameters
in the [0..10] range. They have been remapped to more typical [0..1] ranges in this implementation.
Uses a diffusion stage into a bank of damped delay lines with Hadamard
feedback mixing to emulate the lively, metallic character of multi-spring tanks.
#### Usage
```faust
_ : springreverb(dwell, blend, tone, tension, springs) : _
```
Where:
* `dwell`: feedback amount controlling decay length ([0..1])
* `blend`: wet gain scaling ([0..1], maps to 0..0.8)
* `tone`: lowpass cutoff applied to the wet path ([0..1])
* `tension`: base spring delay time and tail length ([0..1])
* `springs`: spacing preset between spring delays (0 = left, 1 = right, 2 = middle)
#### Test
```faust
re = library("reverbs.lib");
os = library("oscillators.lib");
springreverb_test = os.osc(330)
: re.springreverb(0.5, 0.5, 0.5, 0.5, 1);
```

---

# routes.lib
**Prefix:** `ro`

################################ routes.lib ##########################################
Routing library. Its official prefix is `ro`.

This library provides tools for managing and organizing audio and control signal
routing in Faust. It includes functions for channel mapping, splitting, merging, and
dynamic routing, as well as utilities for building multichannel processing structures.

The Routes library is organized into 1 section:

* [Functions Reference](#functions-reference)

#### References

* <https://github.com/grame-cncm/faustlibraries/blob/master/routes.lib>
########################################################################################

## ro.cross

--------------------------------`(ro.)cross`-----------------------------------
Cross N signals: `(x1,x2,..,xn) -> (xn,..,x2,x1)`.
`cross` is a standard Faust function.
#### Usage
```faust
cross(N)
_,_,_ : cross(3) : _,_,_
```
Where:
* `N`: number of signals (int, as a constant numerical expression)
#### Test
```faust
ro = library("routes.lib");
os = library("oscillators.lib");
cross_test = (os.osc(200), os.osc(300), os.osc(400)) : ro.cross(3);
```
#### Note
Special case: `cross2`:
```faust
cross2 = _,cross(2),_;
```
cross n cables : (x1,x2,..,xn) -> (xn,..,x2,x1)

---

## ro.crossnn

--------------`(ro.)crossnn`--------------
Cross two `bus(N)`s.
#### Usage
```faust
(si.bus(2*N)) : crossnn(N) : (si.bus(2*N))
```
Where:
* `N`: the number of signals in the `bus` (int, as a constant numerical expression)
#### Test
```faust
ro = library("routes.lib");
os = library("oscillators.lib");
crossnn_test = (os.osc(110), os.osc(220), os.osc(330), os.osc(440)) : ro.crossnn(2);
```

---

## ro.crossn1

--------------`(ro.)crossn1`--------------
Cross `bus(N)` and `bus(1)`.
#### Usage
```faust
(si.bus(N),_) : crossn1(N) : (_,si.bus(N))
```
Where:
* `N`: the number of signals in the first `bus` (int, as a constant numerical expression)
#### Test
```faust
ro = library("routes.lib");
os = library("oscillators.lib");
crossn1_test = (os.osc(100), os.osc(200), os.osc(300), os.osc(400)) : ro.crossn1(3);
```

---

## ro.cross1n

--------------`(ro.)cross1n`--------------
Cross `bus(1)` and `bus(N)`.
#### Usage
```faust
(_,si.bus(N)) : crossn1(N) : (si.bus(N),_)
```
Where:
* `N`: the number of signals in the second `bus` (int, as a constant numerical expression)
#### Test
```faust
ro = library("routes.lib");
os = library("oscillators.lib");
cross1n_test = (os.osc(150), os.osc(250), os.osc(350), os.osc(450)) : ro.cross1n(3);
```

---

## ro.crossNM

--------------`(ro.)crossNM`--------------
Cross `bus(N)` and `bus(M)`.
#### Usage
```faust
(si.bus(N),si.bus(M)) : crossNM(N,M) : (si.bus(M),si.bus(N))
```
Where:
* `N`: the number of signals in the first `bus` (int, as a constant numerical expression)
* `M`: the number of signals in the second `bus` (int, as a constant numerical expression)
#### Test
```faust
ro = library("routes.lib");
os = library("oscillators.lib");
crossNM_test = (os.osc(180), os.osc(280), os.osc(380), os.osc(480), os.osc(580)) : ro.crossNM(2,3);
```

---

## ro.interleave

--------------------------`(ro.)interleave`------------------------------
Interleave R x C cables from column order to row order. That is, transpose the input CxR matrix,
the first R inputs is the first row.
input : `x(0), x(1), x(2) ..., x(row*col-1)`
output: `x(0+0*row), x(0+1*row), x(0+2*row), ..., x(1+0*row), x(1+1*row), x(1+2*row), ...`
#### Usage
```faust
si.bus(R*C) : interleave(R,C) : si.bus(R*C)
```
Where:
* `R`: row length (int, as a constant numerical expression)
* `C`: column length (int, as a constant numerical expression)
#### Test
```faust
ro = library("routes.lib");
os = library("oscillators.lib");
interleave_test = (os.osc(200), os.osc(300), os.osc(400), os.osc(500)) : ro.interleave(2,2);
```

---

## ro.butterfly

-------------------------------`(ro.)butterfly`--------------------------------
Addition (first half) then substraction (second half) of interleaved signals.
#### Usage
```faust
si.bus(N) : butterfly(N) : si.bus(N)
```
Where:
* `N`: size of the butterfly (N is int, even and as a constant numerical expression)
#### Test
```faust
ro = library("routes.lib");
os = library("oscillators.lib");
butterfly_test = (os.osc(250), os.osc(350), os.osc(450), os.osc(550)) : ro.butterfly(4);
```

---

## ro.hadamard

------------------------------`(ro.)hadamard`----------------------------------
Hadamard matrix function of size `N = 2^k`.
#### Usage
```faust
si.bus(N) : hadamard(N) : si.bus(N)
```
Where:
* `N`: `2^k`, size of the matrix (int, as a constant numerical expression)
#### Test
```faust
ro = library("routes.lib");
os = library("oscillators.lib");
hadamard_test = (os.osc(220), os.osc(330), os.osc(440), os.osc(550)) : ro.hadamard(4);
```

---

## ro.recursivize

---------------`(ro.)recursivize`-------------
Create a recursion from two arbitrary processors `p` and `q`.
#### Usage
```faust
_,_ : recursivize(p,q) : _,_

```
Where:
* `p`: the forward arbitrary processor
* `q`: the feedback arbitrary processor
#### Test
```faust
ro = library("routes.lib");
os = library("oscillators.lib");
recursivize_test = (os.osc(220), os.osc(330)) : ro.recursivize(*(0.5), *(0.3));
```

---

## ro.bubbleSort

--------------------`(ro.)bubbleSort`-----------------------------------------
Sort a set of N parallel signals in ascending order on-the-fly through
the Bubble Sort algorithm.
Mechanism: having a set of N parallel signals indexed from 0 to N - 1,
compare the first pair of signals and swap them if sig[0] > sig[1];
repeat the pair comparison for the signals sig[1] and sig[2], then again
recursively until reaching the signals sig[N - 2] and sig[N - 1]; by the end,
the largest element in the set will be placed last; repeat the process for
the remaining N - 1 signals until there is a single pair left.
Note that this implementation will always perform the worst-case
computation, O(n^2).
Even though the Bubble Sort algorithm is one of the least efficient ones,
it is a useful example of how automatic sorting can be implemented at the
signal level.
#### Usage
```faust
si.bus(N) : bubbleSort(N) : si.bus(N)

```
Where:
* `N`: the number of signals to be sorted (must be an int >= 0, as a constant numerical expression)
#### Test
```faust
ro = library("routes.lib");
bubbleSort_test = (
hslider("bubbleSort:x0", 0.3, -1, 1, 0.01),
hslider("bubbleSort:x1", -0.2, -1, 1, 0.01),
hslider("bubbleSort:x2", 0.8, -1, 1, 0.01),
hslider("bubbleSort:x3", -0.5, -1, 1, 0.01)
) : ro.bubbleSort(4);
```
#### References
* <https://en.wikipedia.org/wiki/Bubble_sort>

---

# signals.lib
**Prefix:** `si`

################################ signals.lib ##########################################
Signals library. Its official prefix is `si`.

This library provides fundamental signal processing operations for Faust,
including generators, combinators, selectors, and basic DSP utilities. It defines
essential functions used across all Faust libraries for building and manipulating
audio and control signals.

The Signals library is organized into 1 section:

* [Functions Reference](#functions-reference)

#### References

* <https://github.com/grame-cncm/faustlibraries/blob/master/signals.lib>
########################################################################################

## si.bus

--------------------------------`(si.)bus`-------------------------------------
Put N cables in parallel.
`bus` is a standard Faust function.
#### Usage
```faust
bus(N)
bus(4) : _,_,_,_
```
Where:
* `N`: is an integer known at compile time that indicates the number of parallel cables
#### Test
```faust
si = library("signals.lib");
bus_test = (
hslider("bus:x0", 0, -1, 1, 0.01),
hslider("bus:x1", 0, -1, 1, 0.01),
hslider("bus:x2", 0, -1, 1, 0.01)
) : si.bus(3);
```

---

## si.block

--------------`(si.)block`--------------
Block - terminate N signals.
`block` is a standard Faust function.
#### Usage
```faust
si.bus(N) : block(N)
```
Where:
* `N`: the number of signals to be blocked known at compile time
#### Test
```faust
si = library("signals.lib");
block_test = (
hslider("block:x0", 0, -1, 1, 0.01),
hslider("block:x1", 0, -1, 1, 0.01)
) : (si.block(1), _);
```

---

## si.interpolate

-----------------------------`(si.)interpolate`-------------------------------
Linear interpolation between two signals.
#### Usage
```faust
_,_ : interpolate(i) : _
```
Where:
* `i`: interpolation control between 0 and 1 (0: first input; 1: second input)
#### Test
```faust
si = library("signals.lib");
os = library("oscillators.lib");
interpolate_test = si.interpolate(
hslider("interpolate:mix", 0.5, 0, 1, 0.01),
os.osc(220),
os.osc(440)
);
```

---

## si.repeat

---------------`(si.)repeat`----------------------------------------------
Repeat an effect N time(s) and take the parallel sum of all
intermediate buses.
#### Usage
```faust
si.bus(inputs(FX)) : repeat(N, FX) : si.bus(outputs(FX))
```
Where:
* `N`: Number of repetitions, minimum of 1, a constant numerical expression
* `FX`: an arbitrary effect (N inputs and N outputs) that will be repeated
#### Test
```faust
si = library("signals.lib");
repeat_test = hslider("repeat:input", 0, -1, 1, 0.01) : si.repeat(3, *(0.5));
```
Example 1:
```faust
process = repeat(2, dm.zita_light) : _*.5,_*.5;
```
Example 2:
```faust
N = 4;
C = 2;
fx(i) = i+1, par(j, C, @(i*5000));
process = 0, si.bus(C) : repeat(N, fx) : !, par(i, C, _*.2/N);
```
#### References
* <https://github.com/orlarey/presentation-compilateur-faust/blob/master/slides.pdf>

---

## si.smoo

------------------------`(si.)smoo`---------------------------------------
Smoothing function based on `smooth` ideal to smooth UI signals
(sliders, etc.) down. Approximately, this is a 7 Hz one-pole
low-pass considering the coefficient calculation:
exp(-2pi*CF/SR).
`smoo` is a standard Faust function.
#### Usage
```faust
hslider(...) : smoo;
```
#### Test
```faust
si = library("signals.lib");
smoo_test = hslider("smoo:input", 0, -1, 1, 0.01) : si.smoo;
```

---

## si.polySmooth

-----------------------`(si.)polySmooth`--------------------------------
A smoothing function based on `smooth` that doesn't smooth when a
trigger signal is given. This is very useful when making
polyphonic synthesizer to make sure that the value of the parameter
is the right one when the note is started.
#### Usage
```faust
hslider(...) : polySmooth(g,s,d) : _
```
Where:
* `g`: the gate/trigger signal used when making polyphonic synths
* `s`: the smoothness (see `smooth`)
* `d`: the number of samples to wait before the signal start being
smoothed after `g` switched to 1
#### Test
```faust
si = library("signals.lib");
polySmooth_test = hslider("polySmooth:input", 0, -1, 1, 0.01)
: si.polySmooth(button("polySmooth:gate"), 0.999, 32);
```

---

## si.smoothAndH

-----------------------`(si.)smoothAndH`--------------------------------
A smoothing function based on `smooth` that holds its output
signal when a trigger is sent to it. This feature is convenient
when implementing polyphonic instruments to prevent some
smoothed parameter to change when a note-off event is sent.
#### Usage
```faust
hslider(...) : smoothAndH(g,s) : _
```
Where:
* `g`: the hold signal (0 for hold, 1 for bypass)
* `s`: the smoothness (see `smooth`)
#### Test
```faust
si = library("signals.lib");
smoothAndH_test = hslider("smoothAndH:input", 0, -1, 1, 0.01)
: si.smoothAndH(button("smoothAndH:hold"), 0.999);
```

---

## si.bsmooth

-----------------------------`(si.)bsmooth`------------------------------
Block smooth linear interpolation during a block of samples (given by the `ma.BS` value).
#### Usage
```faust
hslider(...) : bsmooth : _
```
#### Test
```faust
si = library("signals.lib");
bsmooth_test = hslider("bsmooth:input", 0, -1, 1, 0.01) : si.bsmooth;
```

---

## si.dot

-------------------------------`(si.)dot`--------------------------------------
Dot product for two vectors of size N.
#### Usage
```faust
si.bus(N), si.bus(N) : dot(N) : _
```
Where:
* `N`: size of the vectors (int, must be known at compile time)
#### Test
```faust
si = library("signals.lib");
os = library("oscillators.lib");
dot_test = (
os.osc(100), os.osc(200), os.osc(300),
os.osc(400), os.osc(500), os.osc(600)
) : si.dot(3);
```

---

## si.smooth

-------------------`(si.)smooth`-----------------------------------
Exponential smoothing by a unity-dc-gain one-pole lowpass.
`smooth` is a standard Faust function.
#### Usage:
```faust
_ : si.smooth(ba.tau2pole(tau)) : _
```
Where:
* `tau`: desired smoothing time constant in seconds, or
```faust
hslider(...) : smooth(s) : _
```
Where:
* `s`: smoothness between 0 and 1. s=0 for no smoothing, s=0.999 is "very smooth",
s>1 is unstable, and s=1 yields the zero signal for all inputs.
The exponential time-constant is approximately 1/(1-s) samples, when s is close to
(but less than) 1.
#### Test
```faust
si = library("signals.lib");
smooth_test = hslider("smooth:input", 0, -1, 1, 0.01) : si.smooth(0.9);
```
#### References
* <https://ccrma.stanford.edu/~jos/mdft/Convolution_Example_2_ADSR.html>
* <https://ccrma.stanford.edu/~jos/aspf/Appendix_B_Inspecting_Assembly.html>
See [grame-cncm/faustlibraries]: Minor improvement to si.smoo. (Discussion #106)

---

## si.smoothq

--------------------------------`(si.)smoothq`-------------------------------------
Smoothing with continuously variable curves from Exponential to Linear, with a constant time.
#### Usage
```faust
_ : smoothq(time, q) : _;
```
Where:
* `time`: seconds to reach target
* `q`: curve shape (between 0..1, 0 is Exponential, 1 is Linear)
#### Test
```faust
si = library("signals.lib");
smoothq_test = hslider("smoothq:input", 0, -1, 1, 0.01) : si.smoothq(0.25, 0.5);
```

---

## si.cbus

--------------------------------`(si.)cbus`-------------------------------------
N parallel cables for complex signals.
`cbus` is a standard Faust function.
#### Usage
```faust
cbus(N)
cbus(4) : (r0,i0), (r1,i1), (r2,i2), (r3,i3)
```
Where:
* `N`: is an integer known at compile time that indicates the number of parallel cables.
* each complex number is represented by two real signals as (real,imag)
#### Test
```faust
si = library("signals.lib");
os = library("oscillators.lib");
cbus_test = (
os.osc(100), os.osc(150),
os.osc(200), os.osc(250)
) : si.cbus(2);
```

---

## si.cmul

--------------------------------`(si.)cmul`-------------------------------------
Multiply two complex signals pointwise.
`cmul` is a standard Faust function.
#### Usage
```faust
(r1,i1) : cmul(r2,i2) : (_,_)
```
Where:
* Each complex number is represented by two real signals as (real,imag), so
- `(r1,i1)` = real and imaginary parts of signal 1
- `(r2,i2)` = real and imaginary parts of signal 2
#### Test
```faust
si = library("signals.lib");
os = library("oscillators.lib");
cmul_test = si.cmul(
os.osc(110), os.osc(220),
os.osc(330), os.osc(440)
);
```

---

## si.cconj

--------------------------------`(si.)cconj`-------------------------------------
Complex conjugation of a (complex) signal.
`cconj` is a standard Faust function.
#### Usage
```faust
(r1,i1) : cconj : (_,_)
```
Where:
* Each complex number is represented by two real signals as (real,imag), so
- `(r1,i1)` = real and imaginary parts of the input signal
- `(r1,-i1)` = real and imaginary parts of the output signal
#### Test
```faust
si = library("signals.lib");
os = library("oscillators.lib");
cconj_test = (os.osc(210), os.osc(310)) : si.cconj;
```

---

## si.onePoleSwitching

-------------`(si.)onePoleSwitching`---------------
One pole filter with independent attack and release times.
#### Usage
```faust
_ : onePoleSwitching(att,rel) : _
```
Where:
* `att`: the attack tau time constant in second
* `rel`: the release tau time constant in second
#### Test
```faust
si = library("signals.lib");
onePoleSwitching_test = hslider("onePoleSwitching:input", 0, -1, 1, 0.01)
: si.onePoleSwitching(0.05, 0.2);
```

---

## si.rev

-------------`(si.)rev`---------------
Reverse the input signal by blocks of n>0 samples. `rev(1)` is the indentity
function. `rev(n)` has a latency of `n-1` samples.
#### Usage
```faust
_ : rev(n) : _
```
Where:
* `n`: the block size in samples
#### Test
```faust
si = library("signals.lib");
os = library("oscillators.lib");
rev_test = os.osc(440) : si.rev(32);
```

---

## si.vecOp

--------------------`(si.)vecOp`----------------------------------------------
This function is a generalisation of Faust's iterators such as `prod` and
`sum`, and it allows to perform operations on an arbitrary number of
vectors, provided that they all have the same length. Unlike Faust's
iterators `prod` and `sum` where the vector size is equal to one and the
vector space dimension must be specified by the user, this function will
infer the vector space dimension and vector size based on the vectors list
that we provide.
The outputs of the function are equal to the vector size, whereas the
number of inputs is dependent on whether the elements of the vectors
provided expect an incoming signal themselves or not. We will see a
clarifying example later; in general, the number of total inputs will
be the sum of the inputs in each input vector.
Note that we must provide a list of at least two vectors, each with a size
that is greater or equal to one.
#### Usage
```faust
si.bus(inputs(vectorsList)) : vecOp((vectorsList), op) : si.bus(outputs(ba.take(1, vectorsList)));
```
#### Where
* `vectorsList`: is a list of vectors
* `op`: is a two-input, one-output operator
#### Test
```faust
si = library("signals.lib");
vecOp_test = si.vecOp((v0, v1), +)
with {
v0 = (hslider("vecOp:v0_0", 0.1, -1, 1, 0.01), hslider("vecOp:v0_1", 0.2, -1, 1, 0.01));
v1 = (hslider("vecOp:v1_0", 0.3, -1, 1, 0.01), hslider("vecOp:v1_1", 0.4, -1, 1, 0.01));
};
```
For example, consider the following vectors lists:
v0 = (0 , 1 , 2 , 3);
v1 = (4 , 5 , 6 , 7);
v2 = (8 , 9 , 10 , 11);
v3 = (12 , 13 , 14 , 15);
v4 = (+(16) , _ , 18 , *(19));
vv = (v0 , v1 , v2 , v3);
Although Faust has limitations for list processing, these vectors can be
combined or processed individually.
If we do:
process = vecOp(v0, +);
the function will deduce a vector space of dimension equal to four and
a vector length equal to one. Note that this is equivalent to writing:
process = v0 : sum(i, 4, _);
Similarly, we can write:
process = vecOp((v0 , v1), *) :> _;
and we have a dimension-two space and length-four vectors. This is the dot
product between vectors v0 and v1, which is equivalent to writing:
process = v0 , v1 : dot(4);
The examples above have no inputs, as none of the elements of the vectors
expect inputs. On the other hand, we can write:
process = vecOp((v4 , v4), +);
and the function will have six inputs and four outputs, as each vector
has three of the four elements expecting an input, times two, as the two
input vectors are identical.
Finally, we can write:
process = vecOp(vv, &);
to perform the bitwise AND on all the elements at the same position in
each vector, having dimension equal to the vector length equal to four.
Or even:
process = vecOp((vv , vv), &);
which gives us a dimension equal to two, and a vector size equal to sixteen.
For a more practical use-case, this is how we can implement a time-invariant
feedback delay network with Hadamard matrix:
N = 4;
normalisation = 1.0 / sqrt(N);
coeffVec = par(i, N, .99 * normalisation);
delVec = par(i, N, (i + 1) * 3);
process = vecOp((si.bus(N) , si.bus(N)), +) ~
vecOp((vecOp((ro.hadamard(N) , coeffVec), *) , delVec), @);

---

## si.bpar

-------------`(si.)bpar`---------------
Balanced `par` where the repeated expression doesn't depend on a variable.
The built-in `par` is implemented as an unbalanced tree, and also has
to substitute the variable into the repeated expression, which is expensive
even when the variable doesn't appear. This version is implemented as a
balanced tree (which allows node reuse during tree traversal) and also
doesn't search for the variable. This can be much faster than `par` to compile.
#### Usage
```faust
si.bus(N * inputs(f)) : bpar(N, f) : si.bus(N * outputs(f))
```
Where:
* `N`: number of repetitions, minimum 1, a constant numerical expression
* `f`: an arbitrary expression
#### Test
```faust
si = library("signals.lib");
os = library("oscillators.lib");
bpar_test = (os.osc(120), os.osc(240), os.osc(360)) : si.bpar(3, *(0.5));
```
Example:
```faust
square each of 4000 inputs
process = si.bpar(4000, (_ <: _, _ : *));
```

---

## si.bsum

-------------`(si.)bsum`---------------
Balanced `sum`, see `si.bpar`.
#### Usage
```faust
si.bus(N * inputs(f)) : bsum(N, f) : _
```
Where:
* `N`: number of repetitions, minimum 1, a constant numerical expression
* `f`: an arbitrary expression with 1 output.
#### Test
```faust
si = library("signals.lib");
os = library("oscillators.lib");
bsum_test = (os.osc(100), os.osc(200), os.osc(300))
: si.bsum(3, *(0.5));
```
Example:
```faust
square each of 1000 inputs and add the results
process = si.bsum(1000, (_ <: _, _ : *));
```

---

## si.bprod

-------------`(si.)bprod`---------------
Balanced `prod`, see `si.bpar`.
#### Usage
```faust
si.bus(N * inputs(f)) : bprod(N, f) : _
```
Where:
* `N`: number of repetitions, minimum 1, a constant numerical expression
* `f`: an arbitrary expression with 1 output.
#### Test
```faust
si = library("signals.lib");
bprod_test = (
hslider("bprod:x0", 0.5, 0, 2, 0.01),
hslider("bprod:x1", 0.8, 0, 2, 0.01)
) : si.bprod(2, _);
```
Example:
```faust
Add 8000 consecutive inputs (in pairs) and multiply the results
process = si.bprod(4000, +);
```

---

# soundfiles.lib
**Prefix:** `so`

################################ soundfiles.lib ##########################################
Soundfiles library. Its official prefix is `so`.

This library provides functions and abstractions to read, write, and manage
audio files in Faust. It supports interpolation and looping controls for integration
of recorded or pre-rendered audio in synthesis, effects, and compositional contexts.

The Soundfiles library is organized into 1 section:

* [Functions Reference](#functions-reference)

#### References

* <https://github.com/grame-cncm/faustlibraries/blob/master/soundfiles.lib>
########################################################################################

## so.loop

--------------------------------`(so.)loop`-----------------------------------
Play a soundfile in a loop taking into account its sampling rate.
`loop` is a standard Faust function.
#### Usage
```faust
loop(sf, part) : si.bus(outputs(sf))
```
Where:
* `sf`: the soundfile
* `part`: the part in the soundfile list of sounds
#### Test
```faust
so = library("soundfiles.lib");
sf = soundfile("sound[url:{'tests/assets/silence.wav'}]", 1);
loop_test = so.loop(sf, 0);
```

---

## so.loop_speed

--------------------------------`(so.)loop_speed`-----------------------------------
Play a soundfile in a loop taking into account its sampling rate, with speed control.
`loop_speed` is a standard Faust function.
#### Usage
```faust
loop_speed(sf, part, speed) : si.bus(outputs(sf))
```
Where:
* `sf`: the soundfile
* `part`: the part in the soundfile list of sounds
* `speed`: the speed between 0 and n
#### Test
```faust
so = library("soundfiles.lib");
sf = soundfile("sound[url:{'tests/assets/silence.wav'}]", 1);
loop_speed_test = so.loop_speed(sf, 0, hslider("loop_speed:speed", 1, 0, 2, 0.01));
```

---

## so.loop_speed_level

--------------------------------`(so.)loop_speed_level`-----------------------------------
Play a soundfile in a loop taking into account its sampling rate, with speed and level controls.
`loop_speed_level` is a standard Faust function.
#### Usage
```faust
loop_speed_level(sf, part, speed, level) : si.bus(outputs(sf))
```
Where:
* `sf`: the soundfile
* `part`: the part in the soundfile list of sounds
* `speed`: the speed between 0 and n
* `level`: the volume between 0 and n
#### Test
```faust
so = library("soundfiles.lib");
sf = soundfile("sound[url:{'tests/assets/silence.wav'}]", 1);
loop_speed_level_test = so.loop_speed_level(
sf,
0,
hslider("loop_speed_level:speed", 1, 0, 2, 0.01),
hslider("loop_speed_level:level", 0.5, 0, 1, 0.01)
);
```

---

# spats.lib
**Prefix:** `sp`

#################################### spats.lib ##########################################
Spatialization (Spats) library. Its official prefix is `sp`.

This library provides spatialization in Faust.
It includes panning and wfs algorithms.

The Spats library is organized into 1 section:

* [Functions Reference](#functions-reference)

#### References

* <https://github.com/grame-cncm/faustlibraries/blob/master/spats.lib>
########################################################################################

## sp.panner

-----------------------`(sp.)panner`------------------------
A simple linear stereo panner.
`panner` is a standard Faust function.
#### Usage
```faust
_ : panner(g) : _,_
```
Where:
* `g`: the panning (0-1)
#### Test
```faust
sp = library("spats.lib");
os = library("oscillators.lib");
panner_test = os.osc(220) : sp.panner(hslider("panner:pan", 0.3, 0, 1, 0.01));
```

---

## sp.constantPowerPan

---------------`(sp.)constantPowerPan`----------------------
Apply the constant power pan rule to a stereo signal.
The channels are not respatialized. Their gains are simply
adjusted. A pan of 0 preserves the left channel and silences
the right channel. A pan of 1 has the opposite effect.
A pan value of 0.5 applies a gain of 0.5 to both channels.
#### Usage
```faust
_,_ : constantPowerPan(p) : _,_
```
Where:
* `p`: the panning (0-1)
#### Test
```faust
sp = library("spats.lib");
os = library("oscillators.lib");
constantPowerPan_test = (os.osc(110), os.osc(220))
: sp.constantPowerPan(hslider("constantPowerPan:pan", 0.4, 0, 1, 0.01));
```

---

## sp.spat

-----------------------`(sp.)spat`------------------------
GMEM SPAT: n-outputs spatializer.
`spat` is a standard Faust function.
#### Usage
```faust
_ : spat(N,r,d) : si.bus(N)
```
Where:
* `N`: number of outputs (a constant numerical expression)
* `r`: rotation (between 0 et 1)
* `d`: distance of the source (between 0 et 1)
#### Test
```faust
sp = library("spats.lib");
os = library("oscillators.lib");
spat_test = os.osc(330)
: sp.spat(4,
hslider("spat:rotation", 0.25, 0, 1, 0.01),
hslider("spat:distance", 0.5, 0, 1, 0.01));
```

---

## sp.wfs

-------`(sp.)wfs`-------------------
Wave Field Synthesis algorithm for multiple sound sources.
Implementation generalized starting from Pierre Lecomte version.
#### Usage
```faust
wfs(xref, yref, zref, speakersDist, nSources, nSpeakers, inProc, xs, ys, zs) : si.bus(nSpeakers)
```
Where:
* `xref`: x-coordinate of the reference listening point in meters
* `yref`: y-coordinate of the reference listening point in meters
* `zref`: z-coordinate of the reference listening point in meters
* `speakersDist`: distance between speakers in meters
* `nSources`: number of sound sources
* `nSpeakers`: number of speakers
* `inProc`: per-source processor function, as a function of the source index
* `xs`: x-coordinate of the sound source in meters, as a function of the source index
* `ys`: y-coordinate of the sound source in meters, as a function of the source index
* `zs`: z-coordinate of the sound source in meters, as a function of the source index
#### Test
```faust
sp = library("spats.lib");
os = library("oscillators.lib");
wfs_proc(i) = *(0.5); // Simple gain processor
wfs_xs(i) = 0.0;
wfs_ys(i) = 1.0;
wfs_zs(i) = 0.0;
wfs_test = os.osc(440)
: sp.wfs(0, 1, 0, 0.5, 1, 2, wfs_inGain, wfs_proc, wfs_xs, wfs_ys, wfs_zs);
```

---

## sp.wfs_ui

-------`(sp.)wfs_ui`-------------------
Wave Field Synthesis algorithm for multiple sound sources with a built-in UI.
#### Usage
```faust
wfs_ui(xref, yref, zref, speakersDist, nSources, nSpeaker) : si.bus(nSpeakers)
```
Where:
* `xref`: x-coordinate of the reference listening point in meters
* `yref`: y-coordinate of the reference listening point in meters
* `zref`: z-coordinate of the reference listening point in meters
* `speakersDist`: distance between speakers in meters
* `nSources`: number of sound sources
* `nSpeakers`: number of speakers
#### Test
```faust
sp = library("spats.lib");
os = library("oscillators.lib");
wfs_ui_test = os.osc(550)
: sp.wfs_ui(0, 1, 0, 0.5, 1, 2);
```
#### Example test program
```faust
Distance between speakers in meters
speakersDist = 0.0783;  

Reference listening point (central position for WFS)
xref = 0;
yref = 1;
zref = 0;

Spatialize 4 sound sources on 16 speakers
process = wfs_ui(xref,yref,zref,speakersDist,4,16);
```

---

## sp.stereoize

---------------`(sp.)stereoize`-------------
Transform an arbitrary processor `p` into a stereo processor with 2 inputs
and 2 outputs.
#### Usage
```faust
_,_ : stereoize(p) : _,_
```
Where:
* `p`: the arbitrary processor
#### Test
```faust
sp = library("spats.lib");
os = library("oscillators.lib");
stereoize_test = (os.osc(660), os.osc(770))
: sp.stereoize(+);
```

---

# stdfaust.lib
**Prefix:** `st`

################################ stdfaust.lib ##########################################
The purpose of this library is to give access to all the Faust standard libraries
through a series of environments.
########################################################################################

# synths.lib
**Prefix:** `sy`

################################ synths.lib ##########################################
Synths library. Its official prefix is `sy`.

This library provides synthesizer and drum building blocks.

The Synths library is organized into 2 sections:

* [Synthesizers](#synthesizers)
* [Drum Synthesis](#drum-synthesis)

#### References

* <https://github.com/grame-cncm/faustlibraries/blob/master/synths.lib>
########################################################################################

## sy.popFilterDrum

-----------------------------------`(sy.)popFilterDrum`--------------------------------------
A simple percussion instrument based on a "popped" resonant bandpass filter.
`popFilterDrum` is a standard Faust function.
#### Usage
```faust
popFilterDrum(freq,q,gate) : _
```
Where:
* `freq`: the resonance frequency of the instrument in Hz
* `q`: the q of the res filter (typically, 5 is a good value)
* `gate`: the trigger signal (0 or 1)
#### Test
```faust
sy = library("synths.lib");
popFilterDrum_test = sy.popFilterDrum(
hslider("popFilterDrum:freq", 200, 50, 1000, 1),
hslider("popFilterDrum:q", 5, 1, 20, 0.1),
button("popFilterDrum:gate")
);
```

---

## sy.dubDub

---------------------------------------`(sy.)dubDub`-----------------------------------------
A simple synth based on a sawtooth wave filtered by a resonant lowpass.
`dubDub` is a standard Faust function.
#### Usage
```faust
dubDub(freq,ctFreq,q,gate) : _
```
Where:
* `freq`: frequency of the sawtooth in Hz
* `ctFreq`: cutoff frequency of the filter
* `q`: Q of the filter
* `gate`: the trigger signal (0 or 1)
#### Test
```faust
sy = library("synths.lib");
dubDub_test = sy.dubDub(
hslider("dubDub:freq", 220, 50, 1000, 1),
hslider("dubDub:cutoff", 800, 100, 6000, 1),
hslider("dubDub:q", 2, 0.2, 10, 0.1),
button("dubDub:gate")
);
```

---

## sy.sawTrombone

-----------------------------------`(sy.)sawTrombone`----------------------------------------
A simple trombone based on a lowpassed sawtooth wave.
`sawTrombone` is a standard Faust function.
#### Usage
```faust
sawTrombone(freq,gain,gate) : _
```
Where:
* `freq`: the frequency in Hz
* `gain`: the gain (0-1)
* `gate`: the gate (0 or 1)
#### Test
```faust
sy = library("synths.lib");
sawTrombone_test = sy.sawTrombone(
hslider("sawTrombone:freq", 196, 50, 600, 1),
hslider("sawTrombone:gain", 0.6, 0, 1, 0.01),
button("sawTrombone:gate")
);
```

---

## sy.combString

-----------------------------------`(sy.)combString`-----------------------------------------
Simplest string physical model ever based on a comb filter.
`combString` is a standard Faust function.
#### Usage
```faust
combString(freq,res,gate) : _
```
Where:
* `freq`: the frequency of the string in Hz
* `res`: string T60 (resonance time) in second
* `gate`: trigger signal (0 or 1)
#### Test
```faust
sy = library("synths.lib");
combString_test = sy.combString(
hslider("combString:freq", 220, 55, 880, 1),
hslider("combString:res", 4, 0.1, 10, 0.01),
button("combString:gate")
);
```

---

## sy.additiveDrum

-----------------------------------`(sy.)additiveDrum`---------------------------------------
A simple drum using additive synthesis.
`additiveDrum` is a standard Faust function.
#### Usage
```faust
additiveDrum(freq,freqRatio,gain,harmDec,att,rel,gate) : _
```
Where:
* `freq`: the resonance frequency of the drum in Hz
* `freqRatio`: a list of ratio to choose the frequency of the mode in
function of `freq` e.g.(1 1.2 1.5 ...). The first element should always
be one (fundamental).
* `gain`: the gain of each mode as a list (1 0.9 0.8 ...). The first element
is the gain of the fundamental.
* `harmDec`: harmonic decay ratio (0-1): configure the speed at which
higher modes decay compare to lower modes.
* `att`: attack duration in second
* `rel`: release duration in second
* `gate`: trigger signal (0 or 1)
#### Test
```faust
sy = library("synths.lib");
additiveDrum_test = sy.additiveDrum(
hslider("additiveDrum:freq", 180, 60, 600, 1),
(1, 1.3, 2.4, 3.2),
(1, 0.8, 0.6, 0.4),
hslider("additiveDrum:harmDec", 0.4, 0, 1, 0.01),
0.01,
0.4,
button("additiveDrum:gate")
);
```

---

## sy.fm

-----------------------------------`(sy.)fm`---------------------------------------
An FM synthesizer with an arbitrary number of modulators connected as a sequence.
`fm` is a standard Faust function.
#### Usage
```faust
freqs = (300,400,...);
indices = (20,...);
fm(freqs,indices) : _
```
Where:
* `freqs`: a list of frequencies where the first one is the frequency of the carrier
and the others, the frequency of the modulator(s)
* `indices`: the indices of modulation (Nfreqs-1)
#### Test
```faust
sy = library("synths.lib");
fm_test = sy.fm((220, 440, 660), (1.5, 0.8));
```

---

## sy.kick

-----------------------------------`(sy.)kick`---------------------------------------
Kick drum synthesis via a pitched sine sweep.
#### Usage
```faust
kick(pitch, click, attack, decay, drive, gate) : _
```
Where:
* `pitch`: the base frequency of the kick drum in Hz
* `click`: the speed of the pitch envelope, tuned for [0.005s, 1s]
* `attack`: attack time in seconds, tuned for [0.005s, 0.4s]
* `decay`: decay time in seconds, tuned for [0.005s, 4.0s]
* `drive`: a gain multiplier going into the saturator. Tuned for [1, 10]
* `gate`: the gate which triggers the amp envelope
#### Test
```faust
sy = library("synths.lib");
kick_test = sy.kick(
hslider("kick:pitch", 60, 30, 120, 0.1),
hslider("kick:click", 0.2, 0.005, 1, 0.001),
0.01,
0.5,
hslider("kick:drive", 3, 1, 10, 0.1),
button("kick:gate")
);
```
#### References
* <https://github.com/nick-thompson/drumsynth/blob/master/kick.js>

---

## sy.clap

-----------------------------------`(sy.)clap`---------------------------------------
Clap synthesis via filtered white noise.
#### Usage
```faust
clap(tone, attack, decay, gate) : _
```
Where:
* `tone`: bandpass filter cutoff frequency, tuned for [400Hz, 3500Hz]
* `attack`: attack time in seconds, tuned for [0s, 0.2s]
* `decay`: decay time in seconds, tuned for [0s, 4.0s]
* `gate`: the gate which triggers the amp envelope
#### Test
```faust
sy = library("synths.lib");
clap_test = sy.clap(
hslider("clap:tone", 1200, 400, 3500, 10),
0.01,
0.6,
button("clap:gate")
);
```
#### References
* <https://github.com/nick-thompson/drumsynth/blob/master/clap.js>

---

## sy.hat

-----------------------------------`(sy.)hat`---------------------------------------
Hi hat drum synthesis via phase modulation.
#### Usage
```faust
hat(pitch, tone, attack, decay, gate): _
```
Where:
* `pitch`: base frequency in the range [317Hz, 3170Hz]
* `tone`: bandpass filter cutoff frequency, tuned for [800Hz, 18kHz]
* `attack`: attack time in seconds, tuned for [0.005s, 0.2s]
* `decay`: decay time in seconds, tuned for [0.005s, 4.0s]
* `gate`: the gate which triggers the amp envelope
#### Test
```faust
sy = library("synths.lib");
hat_test = sy.hat(
hslider("hat:pitch", 800, 317, 3170, 1),
hslider("hat:tone", 5000, 800, 18000, 10),
0.005,
0.3,
button("hat:gate")
);
```
#### References
* <https://github.com/nick-thompson/drumsynth/blob/master/hat.js>

---

# vaeffects.lib
**Prefix:** `ve`

#################################### vaeffects.lib ########################################
Virtual Analog Effects (VAE) library. Its official prefix is `ve`.

This library provides virtual analog (VA) audio effects modeled after classic
analog circuitry. It includes nonlinear filters and effects.

The virtual analog filter library is organized into 7 sections:

* [Moog Filters](#moog-filters)
* [Korg 35 Filters](#korg-35-filters)
* [Oberheim Filters](#oberheim-filters)
* [Sallen Key Filters](#sallen-key-filters)
* [Korg 35 Filters](#korg-35-filters)
* [Vicanek's matched (decramped) second-order filters](#vicaneks-matched-decramped-second-order-filters)
* [Effects](#effects)

#### References

* <https://github.com/grame-cncm/faustlibraries/blob/master/vaeffects.lib>
########################################################################################

## ve.moog_vcf

-------------------------`(ve.)moog_vcf`---------------------------
Moog "Voltage Controlled Filter" (VCF) in "analog" form. Moog VCF
implemented using the same logical block diagram as the classic
analog circuit.  As such, it neglects the one-sample delay associated
with the feedback path around the four one-poles.
This extra delay alters the response, especially at high frequencies
(see reference [1] for details).
See `moog_vcf_2b` below for a more accurate implementation.
#### Usage
```faust
_ : moog_vcf(res,fr) : _
```
Where:
* `res`: normalized amount of corner-resonance between 0 and 1
(0 is no resonance, 1 is maximum)
* `fr`: corner-resonance frequency in Hz (less than SR/6.3 or so)
#### Test
```faust
ve = library("vaeffects.lib");
os = library("oscillators.lib");
moog_vcf_test = os.osc(440)
: ve.moog_vcf(
hslider("moog_vcf:res", 0.5, 0, 1, 0.01),
hslider("moog_vcf:freq", 1000, 50, 4000, 1)
);
```
#### References
* <https://ccrma.stanford.edu/~stilti/papers/moogvcf.pdf>
* <https://ccrma.stanford.edu/~jos/pasp/vegf.html>

---

## ve.moogLadder

------------------`(ve.)moogLadder`-----------------
Virtual analog model of the 4th-order Moog Ladder (without any nonlinearities), which is arguably the
most well-known ladder filter in analog synthesizers. Several
1st-order filters are cascaded in series. Feedback is then used, in part, to
control the cut-off frequency and the resonance.
#### Usage
```faust
_ : moogLadder(normFreq,Q) : _
```
Where:
* `normFreq`: normalized frequency (0-1)
* `Q`: quality factor between .707 (0 feedback coefficient) to 25 (feedback = 4, which is the self-oscillating threshold).
#### Test
```faust
ve = library("vaeffects.lib");
os = library("oscillators.lib");
moogLadder_test = os.osc(220)
: ve.moogLadder(
hslider("moogLadder:normFreq", 0.3, 0, 1, 0.001),
hslider("moogLadder:Q", 4, 0.7, 20, 0.1)
);
```
#### References
* [Zavalishin 2012] (revision 2.1.2, February 2020)
* <https://www.native-instruments.com/fileadmin/ni_media/downloads/pdf/VAFilterDesign_2.1.2.pdf>
* Lorenzo Della Cioppa's correction to Pirkle's implementation: <https://www.kvraudio.com/forum/viewtopic.php?f=33&t=571909>

---

## ve.lowpassLadder4

------------------`(ve.)lowpassLadder4`-----------------
Topology-preserving transform implementation of a four-pole ladder lowpass.
This is essentially the same filter as the moogLadder above except for
the parameters, which will be expressed in Hz, for the cutoff, and as a
raw feedback coefficient, for the resonance.
Also, note that the parameter order has changed.
#### Usage
```faust
_ : lowpassLadder4(k, CF) : _
```
Where:
* `k`: feedback coefficient between 0 and 4, which is the stability threshold.
* `CF`: the filter's cutoff in Hz.
#### Test
```faust
ve = library("vaeffects.lib");
os = library("oscillators.lib");
lowpassLadder4_test = os.osc(110)
: ve.lowpassLadder4(
hslider("lowpassLadder4:k", 2.0, 0, 4, 0.1),
hslider("lowpassLadder4:freq", 800, 50, 5000, 1)
);
```
Notes:
If you want to express the feedback coefficient as the resonance peak, you can use the formula:
k = 4.0 - 1.0 / Q;
where Q, between .25 and infinity, corresponds to the peak of the filter at cutoff.
I.e., if you feed the filter with a sine whose frequency is the same as the cutoff, the output
peak corresponds exactly to that set via the Q-param.
#### References
* [Zavalishin 2012] (revision 2.1.2, February 2020)
* <https://www.native-instruments.com/fileadmin/ni_media/downloads/pdf/VAFilterDesign_2.1.2.pdf>

---

## ve.moogHalfLadder

------------------`(ve.)moogHalfLadder`-----------------
Virtual analog model of the 2nd-order Moog Half Ladder (simplified version of
`(ve.)moogLadder`). Several 1st-order filters are cascaded in series.
Feedback is then used, in part, to control the cut-off frequency and the
resonance.
This filter was implemented in Faust by Eric Tarr during the
[2019 Embedded DSP With Faust Workshop](https://ccrma.stanford.edu/workshops/faust-embedded-19/).
#### Usage
```faust
_ : moogHalfLadder(normFreq,Q) : _
```
Where:
* `normFreq`: normalized frequency (0-1)
* `Q`: q
#### Test
```faust
ve = library("vaeffects.lib");
os = library("oscillators.lib");
moogHalfLadder_test = os.osc(220)
: ve.moogHalfLadder(
hslider("moogHalfLadder:normFreq", 0.3, 0, 1, 0.001),
hslider("moogHalfLadder:Q", 4, 0.7, 20, 0.1)
);
```
#### References
* <https://www.willpirkle.com/app-notes/virtual-analog-moog-half-ladder-filter>
* <http://www.willpirkle.com/Downloads/AN-8MoogHalfLadderFilter.pdf>

---

## ve.diodeLadder

------------------`(ve.)diodeLadder`-----------------
4th order virtual analog diode ladder filter. In addition to the individual
states used within each independent 1st-order filter, there are also additional
feedback paths found in the block diagram. These feedback paths are labeled
as connecting states. Rather than separately storing these connecting states
in the Faust implementation, they are simply implicitly calculated by
tracing back to the other states (`s1`,`s2`,`s3`,`s4`) each recursive step.
This filter was implemented in Faust by Eric Tarr during the
[2019 Embedded DSP With Faust Workshop](https://ccrma.stanford.edu/workshops/faust-embedded-19/).
#### Usage
```faust
_ : diodeLadder(normFreq,Q) : _
```
Where:
* `normFreq`: normalized frequency (0-1)
* `Q`: q
#### Test
```faust
ve = library("vaeffects.lib");
os = library("oscillators.lib");
diodeLadder_test = os.osc(220)
: ve.diodeLadder(
hslider("diodeLadder:normFreq", 0.4, 0, 1, 0.001),
hslider("diodeLadder:Q", 4, 0.7, 20, 0.1)
);
```
#### References
* <https://www.willpirkle.com/virtual-analog-diode-ladder-filter/>
* <http://www.willpirkle.com/Downloads/AN-6DiodeLadderFilter.pdf>

---

## ve.korg35LPF

------------------`(ve.)korg35LPF`-----------------
Virtual analog models of the Korg 35 low-pass filter found in the MS-10 and
MS-20 synthesizers.
#### Usage
```faust
_ : korg35LPF(normFreq,Q) : _
```
Where:
* `normFreq`: normalized frequency (0-1)
* `Q`: q
#### Test
```faust
ve = library("vaeffects.lib");
os = library("oscillators.lib");
korg35LPF_test = os.osc(220)
: ve.korg35LPF(
hslider("korg35LPF:normFreq", 0.35, 0, 1, 0.001),
hslider("korg35LPF:Q", 3.5, 0.7, 10, 0.1)
);
```

---

## ve.korg35HPF

------------------`(ve.)korg35HPF`-----------------
Virtual analog models of the Korg 35 high-pass filter found in the MS-10 and
MS-20 synthesizers.
#### Usage
```faust
_ : korg35HPF(normFreq,Q) : _
```
Where:
* `normFreq`: normalized frequency (0-1)
* `Q`: q
#### Test
```faust
ve = library("vaeffects.lib");
os = library("oscillators.lib");
korg35HPF_test = os.osc(330)
: ve.korg35HPF(
hslider("korg35HPF:normFreq", 0.4, 0, 1, 0.001),
hslider("korg35HPF:Q", 3.5, 0.7, 10, 0.1)
);
```

---

## ve.oberheim

------------------`(ve.)oberheim`-----------------
Generic multi-outputs Oberheim filter that produces the BSF, BPF, HPF and LPF outputs (see description above).
#### Usage
```faust
_ : oberheim(normFreq,Q) : _,_,_,_
```
Where:
* `normFreq`: normalized frequency (0-1)
* `Q`: q
#### Test
```faust
ve = library("vaeffects.lib");
os = library("oscillators.lib");
oberheim_test = os.osc(220)
: ve.oberheim(
hslider("oberheim:normFreq", 0.4, 0, 1, 0.001),
hslider("oberheim:Q", 1.5, 0.5, 10, 0.1)
);
```

---

## ve.oberheimBSF

------------------`(ve.)oberheimBSF`-----------------
Band-Stop Oberheim filter (see description above).
Specialize the generic implementation: keep the first BSF output,
the compiler will only generate the needed code.
#### Usage
```faust
_ : oberheimBSF(normFreq,Q) : _
```
Where:
* `normFreq`: normalized frequency (0-1)
* `Q`: q
#### Test
```faust
ve = library("vaeffects.lib");
os = library("oscillators.lib");
oberheimBSF_test = os.osc(220)
: ve.oberheimBSF(
hslider("oberheimBSF:normFreq", 0.4, 0, 1, 0.001),
hslider("oberheimBSF:Q", 1.5, 0.5, 10, 0.1)
);
```

---

## ve.oberheimBPF

------------------`(ve.)oberheimBPF`-----------------
Band-Pass Oberheim filter (see description above).
Specialize the generic implementation: keep the second BPF output,
the compiler will only generate the needed code.
#### Usage
```faust
_ : oberheimBPF(normFreq,Q) : _
```
Where:
* `normFreq`: normalized frequency (0-1)
* `Q`: q
#### Test
```faust
ve = library("vaeffects.lib");
os = library("oscillators.lib");
oberheimBPF_test = os.osc(220)
: ve.oberheimBPF(
hslider("oberheimBPF:normFreq", 0.4, 0, 1, 0.001),
hslider("oberheimBPF:Q", 1.5, 0.5, 10, 0.1)
);
```

---

## ve.oberheimHPF

------------------`(ve.)oberheimHPF`-----------------
High-Pass Oberheim filter (see description above).
Specialize the generic implementation: keep the third HPF output,
the compiler will only generate the needed code.
#### Usage
```faust
_ : oberheimHPF(normFreq,Q) : _
```
Where:
* `normFreq`: normalized frequency (0-1)
* `Q`: q
#### Test
```faust
ve = library("vaeffects.lib");
os = library("oscillators.lib");
oberheimHPF_test = os.osc(220)
: ve.oberheimHPF(
hslider("oberheimHPF:normFreq", 0.4, 0, 1, 0.001),
hslider("oberheimHPF:Q", 1.5, 0.5, 10, 0.1)
);
```

---

## ve.oberheimLPF

------------------`(ve.)oberheimLPF`-----------------
Low-Pass Oberheim filter (see description above).
Specialize the generic implementation: keep the fourth LPF output,
the compiler will only generate the needed code.
#### Usage
```faust
_ : oberheimLPF(normFreq,Q) : _
```
Where:
* `normFreq`: normalized frequency (0-1)
* `Q`: q
#### Test
```faust
ve = library("vaeffects.lib");
os = library("oscillators.lib");
oberheimLPF_test = os.osc(220)
: ve.oberheimLPF(
hslider("oberheimLPF:normFreq", 0.4, 0, 1, 0.001),
hslider("oberheimLPF:Q", 1.5, 0.5, 10, 0.1)
);
```

---

## ve.sallenKeyOnePole

------------------`(ve.)sallenKeyOnePole`-----------------
Sallen-Key generic One Pole filter that produces the LPF and HPF outputs (see description above).
For the Faust implementation of this filter, recursion (`letrec`) is used
for storing filter "states". The output (e.g. `y`) is calculated by using
the input signal and the previous states of the filter.
During the current recursive step, the states of the filter (e.g. `s`) for
the next step are also calculated.
Admittedly, this is not an efficient way to implement a filter because it
requires independently calculating the output and each state during each
recursive step. However, it works as a way to store and use "states"
within the constraints of Faust.
The simplest example is the 1st-order LPF (shown on the cover of Zavalishin
2018 and Fig 4.3 of <https://www.willpirkle.com/706-2/>).
Here, the input signal is split in parallel for the calculation of the output signal, `y`,
and the state `s`. The value of the state is only used for feedback to the next
step of recursion. It is blocked (!) from also being routed to the output.
A trick used for calculating the state `s` is to observe that the input to
the delay block is the sum of two signal: what appears to be a feedforward
path and a feedback path. In reality, the signals being summed are identical
`(signal*2)` plus the value of the current state.
#### Usage
```faust
_ : sallenKeyOnePole(normFreq) : _,_
```
Where:
* `normFreq`: normalized frequency (0-1)
#### Test
```faust
ve = library("vaeffects.lib");
os = library("oscillators.lib");
sallenKeyOnePole_test = os.osc(440)
: ve.sallenKeyOnePole(
hslider("sallenKeyOnePole:normFreq", 0.25, 0, 1, 0.001)
);
```

---

## ve.sallenKeyOnePoleLPF

------------------`(ve.)sallenKeyOnePoleLPF`-----------------
Sallen-Key One Pole lowpass filter (see description above).
Specialize the generic implementation: keep the first LPF output,
the compiler will only generate the needed code.
#### Usage
```faust
_ : sallenKeyOnePoleLPF(normFreq) : _
```
Where:
* `normFreq`: normalized frequency (0-1)
#### Test
```faust
ve = library("vaeffects.lib");
os = library("oscillators.lib");
sallenKeyOnePoleLPF_test = os.osc(440)
: ve.sallenKeyOnePoleLPF(
hslider("sallenKeyOnePoleLPF:normFreq", 0.25, 0, 1, 0.001)
);
```

---

## ve.sallenKeyOnePoleHPF

------------------`(ve.)sallenKeyOnePoleHPF`-----------------
Sallen-Key One Pole Highpass filter (see description above). The dry input
signal is routed in parallel to the output. The LPF'd signal is subtracted
from the input so that the HPF remains.
Specialize the generic implementation: keep the second HPF output,
the compiler will only generate the needed code.
#### Usage
```faust
_ : sallenKeyOnePoleHPF(normFreq) : _
```
Where:
* `normFreq`: normalized frequency (0-1)
#### Test
```faust
ve = library("vaeffects.lib");
os = library("oscillators.lib");
sallenKeyOnePoleHPF_test = os.osc(440)
: ve.sallenKeyOnePoleHPF(
hslider("sallenKeyOnePoleHPF:normFreq", 0.25, 0, 1, 0.001)
);
```

---

## ve.sallenKey2ndOrder

------------------`(ve.)sallenKey2ndOrder`-----------------
Sallen-Key generic 2nd order filter that produces the LPF, BPF and HPF outputs.
This is a 2nd-order Sallen-Key state-variable filter. The idea is that by
"tapping" into different points in the circuit, different filters
(LPF,BPF,HPF) can be achieved. See Figure 4.6 of
<https://www.willpirkle.com/706-2/>
This is also a good example of the next step for generalizing the Faust
programming approach used for all these VA filters. In this case, there are
three things to calculate each recursive step (`y`,`s1`,`s2`). For each thing, the
circuit is only calculated up to that point.
Comparing the LPF to BPF, the output signal (`y`) is calculated similarly.
Except, the output of the BPF stops earlier in the circuit. Similarly, the
states (`s1` and `s2`) only differ in that `s2` includes a couple more terms
beyond what is used for `s1`.
#### Usage
```faust
_ : sallenKey2ndOrder(normFreq,Q) : _,_,_
```
Where:
* `normFreq`: normalized frequency (0-1)
* `Q`: quality factor controlling the sharpness/resonance of the filter around the center frequency (CF). For bandpass filters, higher Q increases the gain at the center frequency. Must be in the range `[ma.EPSILON, ma.MAX]`
#### Test
```faust
ve = library("vaeffects.lib");
os = library("oscillators.lib");
sallenKey2ndOrder_test = os.osc(330)
: ve.sallenKey2ndOrder(
hslider("sallenKey2ndOrder:normFreq", 0.3, 0, 1, 0.001),
hslider("sallenKey2ndOrder:Q", 1.0, 0.1, 10, 0.1)
);
```

---

## ve.sallenKey2ndOrderLPF

------------------`(ve.)sallenKey2ndOrderLPF`-----------------
Sallen-Key 2nd order lowpass filter (see description above).
Specialize the generic implementation: keep the first LPF output,
the compiler will only generate the needed code.
#### Usage
```faust
_ : sallenKey2ndOrderLPF(normFreq,Q) : _
```
Where:
* `normFreq`: normalized frequency (0-1)
* `Q`: quality factor controlling the sharpness/resonance of the filter around the center frequency (CF). For bandpass filters, higher Q increases the gain at the center frequency. Must be in the range `[ma.EPSILON, ma.MAX]`
#### Test
```faust
ve = library("vaeffects.lib");
os = library("oscillators.lib");
sallenKey2ndOrderLPF_test = os.osc(330)
: ve.sallenKey2ndOrderLPF(
hslider("sallenKey2ndOrderLPF:normFreq", 0.3, 0, 1, 0.001),
hslider("sallenKey2ndOrderLPF:Q", 0.8, 0.1, 10, 0.1)
);
```

---

## ve.sallenKey2ndOrderBPF

------------------`(ve.)sallenKey2ndOrderBPF`-----------------
Sallen-Key 2nd order bandpass filter (see description above).
Specialize the generic implementation: keep the second BPF output,
the compiler will only generate the needed code.
#### Usage
```faust
_ : sallenKey2ndOrderBPF(normFreq,Q) : _
```
Where:
* `normFreq`: normalized frequency (0-1)
* `Q`: quality factor controlling the sharpness/resonance of the filter around the center frequency (CF). For bandpass filters, higher Q increases the gain at the center frequency. Must be in the range `[ma.EPSILON, ma.MAX]`
#### Test
```faust
ve = library("vaeffects.lib");
os = library("oscillators.lib");
sallenKey2ndOrderBPF_test = os.osc(330)
: ve.sallenKey2ndOrderBPF(
hslider("sallenKey2ndOrderBPF:normFreq", 0.3, 0, 1, 0.001),
hslider("sallenKey2ndOrderBPF:Q", 1.5, 0.1, 10, 0.1)
);
```

---

## ve.sallenKey2ndOrderHPF

------------------`(ve.)sallenKey2ndOrderHPF`-----------------
Sallen-Key 2nd order highpass filter (see description above).
Specialize the generic implementation: keep the third HPF output,
the compiler will only generate the needed code.
#### Usage
```faust
_ : sallenKey2ndOrderHPF(normFreq,Q) : _
```
Where:
* `normFreq`: normalized frequency (0-1)
* `Q`: quality factor controlling the sharpness/resonance of the filter around the center frequency (CF). For bandpass filters, higher Q increases the gain at the center frequency. Must be in the range `[ma.EPSILON, ma.MAX]`
#### Test
```faust
ve = library("vaeffects.lib");
os = library("oscillators.lib");
sallenKey2ndOrderHPF_test = os.osc(330)
: ve.sallenKey2ndOrderHPF(
hslider("sallenKey2ndOrderHPF:normFreq", 0.3, 0, 1, 0.001),
hslider("sallenKey2ndOrderHPF:Q", 0.8, 0.1, 10, 0.1)
);
```

---

## ve.biquad

----------`(ve.)biquad`-------------------------------------------------------
Basic biquad section implementing the difference equation:
`y[n] = b0 * x[n] + b1 * x[n-1] + b2 * x[n-2] - a1 * y[n-1] - a2 * y[n-2]`
#### Usage:
```faust
_ : biquad(b0, b1, b2, a1, a2) : _
```
Where:
* `b0, b1, b2, a1, a2` are the coefficients of the difference equation above
#### Test
```faust
ve = library("vaeffects.lib");
os = library("oscillators.lib");
biquad_test = os.osc(440)
: ve.biquad(0.5, 0.3, 0.2, -0.3, 0.2);
```

---

## ve.lowpass2Matched

----------`(ve.)lowpass2Matched`----------------------------------------------
Vicanek's decramped second-order resonant lowpass filter.
⚠️ **Note:** These filters require **double-precision** support.
#### Usage:
```faust
_ : lowpass2Matched(CF, Q) : _
```
Where:
* `CF`: cutoff frequency in Hz
* `Q`: resonance linear amplitude
#### Test
```faust
ve = library("vaeffects.lib");
os = library("oscillators.lib");
lowpass2Matched_test = os.osc(440)
: ve.lowpass2Matched(
hslider("lowpass2Matched:CF", 1000, 50, 5000, 1),
hslider("lowpass2Matched:Q", 0.707, 0.1, 5, 0.01)
);
```

---

## ve.highpass2Matched

----------`(ve.)highpass2Matched`----------------------------------------------
Vicanek's decramped second-order resonant highpass filter.
⚠️ **Note:** These filters require **double-precision** support.
#### Usage:
```faust
_ : highpass2Matched(CF, Q) : _
```
Where:
* `CF`: cutoff frequency in Hz
* `Q`: resonance linear amplitude
#### Test
```faust
ve = library("vaeffects.lib");
os = library("oscillators.lib");
highpass2Matched_test = os.osc(440)
: ve.highpass2Matched(
hslider("highpass2Matched:CF", 500, 50, 5000, 1),
hslider("highpass2Matched:Q", 0.707, 0.1, 5, 0.01)
);
```

---

## ve.bandpass2Matched

----------`(ve.)bandpass2Matched`----------------------------------------------
Vicanek's decramped second-order resonant bandpass filter.
⚠️ **Note:** These filters require **double-precision** support.
#### Usage:
```faust
_ : bandpass2Matched(CF, Q) : _
```
Where:
* `CF`: cutoff frequency in Hz
* `Q`: peak width
#### Test
```faust
ve = library("vaeffects.lib");
os = library("oscillators.lib");
bandpass2Matched_test = os.osc(440)
: ve.bandpass2Matched(
hslider("bandpass2Matched:CF", 1200, 50, 5000, 1),
hslider("bandpass2Matched:Q", 2.0, 0.1, 10, 0.01)
);
```

---

## ve.peaking2Matched

----------`(ve.)peaking2Matched`----------------------------------------------
Vicanek's decramped second-order resonant bandpass filter.
⚠️ **Note:** These filters require **double-precision** support.
#### Usage:
```faust
_ : peaking2Matched(G, CF, Q) : _
```
Where:
* `G`: peak linear amplitude
* `CF`: cutoff frequency in Hz
* `Q`: peak width
#### Test
```faust
ve = library("vaeffects.lib");
os = library("oscillators.lib");
peaking2Matched_test = os.osc(440)
: ve.peaking2Matched(
hslider("peaking2Matched:G", 1.5, 0.1, 4, 0.01),
hslider("peaking2Matched:CF", 1000, 50, 5000, 1),
hslider("peaking2Matched:Q", 2.0, 0.1, 10, 0.01)
);
```

---

## ve.lowshelf2Matched

----------`(ve.)lowshelf2Matched`---------------------------------------------
Vicanek's decramped second-order Butterworth lowshelf filter.
⚠️ **Note:** These filters require **double-precision** support.
#### Usage:
```faust
_ : lowshelf2Matched(G, CF) : _
```
Where:
* `G`: shelf linear amplitude
* `CF`: cutoff frequency in Hz
#### Test
```faust
ve = library("vaeffects.lib");
os = library("oscillators.lib");
lowshelf2Matched_test = os.osc(330)
: ve.lowshelf2Matched(
hslider("lowshelf2Matched:G", 1.5, 0.5, 4, 0.01),
hslider("lowshelf2Matched:CF", 500, 50, 5000, 1)
);
```

---

## ve.highshelf2Matched

----------`(ve.)highshelf2Matched`--------------------------------------------
Vicanek's decramped second-order Butterworth highshelf filter.
⚠️ **Note:** These filters require **double-precision** support.
#### Usage:
```faust
_ : highshelf2Matched(G, CF) : _
```
Where:
* `G`: shelf linear amplitude
* `CF`: cutoff frequency in Hz
#### Test
```faust
ve = library("vaeffects.lib");
os = library("oscillators.lib");
highshelf2Matched_test = os.osc(330)
: ve.highshelf2Matched(
hslider("highshelf2Matched:G", 1.5, 0.5, 4, 0.01),
hslider("highshelf2Matched:CF", 1500, 50, 10000, 1)
);
```

---

## ve.wah4

--------------------------`(ve.)wah4`-------------------------------
Wah effect, 4th order.
`wah4` is a standard Faust function.
#### Usage
```faust
_ : wah4(fr) : _
```
Where:
* `fr`: resonance frequency in Hz
#### Test
```faust
ve = library("vaeffects.lib");
os = library("oscillators.lib");
wah4_test = os.osc(220)
: ve.wah4(
hslider("wah4:freq", 800, 200, 2000, 1)
);
```
#### References
* <https://ccrma.stanford.edu/~jos/pasp/vegf.html>

---

## ve.autowah

------------------------`(ve.)autowah`-----------------------------
Auto-wah effect.
`autowah` is a standard Faust function.
#### Usage
```faust
_ : autowah(level) : _
```
Where:
* `level`: amount of effect desired (0 to 1).
#### Test
```faust
ve = library("vaeffects.lib");
os = library("oscillators.lib");
autowah_test = os.osc(220)
: ve.autowah(
hslider("autowah:level", 0.7, 0, 1, 0.01)
);
```

---

## ve.crybaby

--------------------------`(ve.)crybaby`-----------------------------
Digitized CryBaby wah pedal.
`crybaby` is a standard Faust function.
#### Usage
```faust
_ : crybaby(wah) : _
```
Where:
* `wah`: "pedal angle" from 0 to 1
#### Test
```faust
ve = library("vaeffects.lib");
os = library("oscillators.lib");
crybaby_test = os.osc(220)
: ve.crybaby(
hslider("crybaby:wah", 0.3, 0, 1, 0.01)
);
```
#### References
* <https://ccrma.stanford.edu/~jos/pasp/vegf.html>

---

## ve.vocoder

----------------------------`(ve.)vocoder`-------------------------
A very simple vocoder where the spectrum of the modulation signal
is analyzed using a filter bank.
`vocoder` is a standard Faust function.
#### Usage
```faust
_ : vocoder(nBands,att,rel,BWRatio,source,excitation) : _
```
Where:
* `nBands`: Number of vocoder bands
* `att`: Attack time in seconds
* `rel`: Release time in seconds
* `BWRatio`: Coefficient to adjust the bandwidth of each band (0.1 - 2)
* `source`: Modulation signal
* `excitation`: Excitation/Carrier signal
#### Test
```faust
ve = library("vaeffects.lib");
no = library("noises.lib");
os = library("oscillators.lib");
vocoder_test = (no.noise, os.osc(220))
: ve.vocoder(
8,
hslider("vocoder:att", 0.01, 0.001, 0.1, 0.001),
hslider("vocoder:rel", 0.1, 0.01, 0.5, 0.01),
hslider("vocoder:BWRatio", 1.0, 0.5, 1.5, 0.01)
);
```

---

# version.lib
**Prefix:** `vl`

################################ version.lib ##########################################
Semantic versioning for the Faust libraries. Its official prefix is `vl`.

#### References

* <https://github.com/grame-cncm/faustlibraries/blob/master/version.lib>
########################################################################################
---------------------------`(vl.)version`---------------------------
Return the version number of the Faust standard libraries as a MAJOR, MINOR, PATCH versioning triplet.

#### Usage

```
version : _,_,_
```

------------------------------------------------------------

## vl.version

---------------------------`(vl.)version`---------------------------
Return the version number of the Faust standard libraries as a MAJOR, MINOR, PATCH versioning triplet.
#### Usage
```faust
version : _,_,_
```

---

# wdmodels.lib
**Prefix:** `wd`

#################################### wdmodels.lib ##############################################################################
A library of basic adaptors and methods to help construct Wave Digital Filter models in Faust. Its official prefix is `wd`.

The WDM library is organized into 8 sections:

* [Algebraic One Port Adaptors](#algebraic-one-port-adaptors)
* [Reactive One Port Adaptors](#reactive-one-port-adaptors)
* [Nonlinear One Port Adaptors](#nonlinear-one-port-adaptors)
* [Two Port Adaptors](#two-port-adaptors)
* [Three Port Adaptors](#three-port-adaptors)
* [R-Type Adaptors](#r-type-adaptors)
* [Node Creating Functions](#node-creating-functions)
* [Model Building Functions](#model-building-functions)

## Library ReadMe
This library is intended for use for creating Wave Digital (WD) based models of audio circuitry for real-time audio processing within the Faust programming language. The goal is to provide a framework to create real-time virtual-analog audio effects and synthesizers using WD models without the use of C++. Furthermore, we seek to provide access to the technique of WD modeling to those without extensive knowledge of advanced digital signal processing techniques. Finally, we hope to provide a library which can integrate with all aspects of Faust, thus creating a platform for virtual circuit bending.
The library itself is written in Faust to maintain portability.

This library is heavily based on Kurt Werner's Dissertation, "Virtual Analog Modeling of Audio Circuitry Using Wave Digital Filters." I have tried to maintain consistent notation between the adaptors appearing within thesis and my adaptor code. The majority of the adaptors found in chapter 1 and chapter 3 are currently supported.

For inquires about use of this library in a commercial product, please contact dirk [dot] roosenburg [dot] 30 [at] gmail [dot] com.
This documentation is taken directly from the [readme](https://github.com/droosenb/faust-wdf-library). Please refer to it for a more updated version.

Many of the more in depth comments within the library include jargon. I plan to create videos detailing the theory of WD models.
For now I recommend Kurt Werner's PhD, [Virtual analog modeling of Audio circuitry using Wave Digital Filters](https://searchworks.stanford.edu/view/11891203).
I have tried to maintain consistent syntax and notation to the thesis.
This library currently includes the majority of the adaptors covered in chapter 1 and some from chapter 3.


## Using this Library

Use of this library expects some level of familiarity with WDF techniques, especially simplification and decomposition of electronic circuits into WDF connection trees. I plan to create video to cover both these techniques and use of the library.

### Quick Start

To get a quick overview of the library, start with the `secondOrderFilters.dsp` code found in [examples](https://github.com/droosenb/faust-wdf-library/tree/main/examples).
Note that the `wdmodels.lib` library is now embedded in the [online Faust IDE](https://faustide.grame.fr/).

### A Simple RC Filter Model

Creating a model using this library consists fo three steps. First, declare a set of components.
Second, model the relationship between them using a tree. Finally, build the tree using the libraries build functions.

First, a set of components is declared using adaptors from the library.
This list of components is created based on analysis of the circuit using WDF techniques,
though generally each circuit element (resistor, capacitor, diode, etc.) can be expected to appear
within the component set. For example, first order RC lowpass filter would require an unadapted voltage source,
a 47k resistor, and a 10nF capacitor which outputs the voltage across itself. These can be declared with:


## wd.resistor

----------------------`(wd.)resistor`--------------------------
Adapted Resistor.
A basic node implementing a resistor for use within Wave Digital Filter connection trees.
It should be used as a leaf/terminating element of the connection tree.
#### Usage
```faust
r1(i) = resistor(i, R);
buildtree( A : r1 );
```
Where:
* `i`: index used by model-building functions. Should never be user declared.
* `R` : Resistance/Impedance of the resistor being modeled in Ohms.
#### Test
```faust
wd = library("wdmodels.lib");
os = library("oscillators.lib");

drive = os.osc(220);

vsrc(i) = wd.u_voltage(i, drive);
series_node(i) = wd.series(i);
res_leaf(i) = wd.resistor(i, 1000);
probe(i) = wd.resistor_Vout(i, 1000);

resistor_test = wd.buildtree(vsrc : (series_node : (res_leaf, probe)));
```
Note: the adaptor must be declared as a separate function before integration into the connection tree.
Correct implementation is shown above.
#### References
K. Werner, "Virtual Analog Modeling of Audio Circuitry Using Wave Digital Filters", 1.2.1

---

## wd.resistor_Vout

----------------------`(wd.)resistor_Vout`--------------------------
Adapted Resistor + voltage Out.
A basic adaptor implementing a resistor for use within Wave Digital Filter connection trees.
It should be used as a leaf/terminating element of the connection tree.
The resistor will also pass the voltage across itself as an output of the model.
#### Usage
```faust
rout(i) = resistor_Vout(i, R);
buildtree( A : rout ) : _
```
Where:
* `i`: index used by model-building functions. Should never be user declared.
* `R` : Resistance/Impedance of the resistor being modeled in Ohms.
#### Test
```faust
wd = library("wdmodels.lib");
os = library("oscillators.lib");

drive = os.osc(220);

vsrc(i) = wd.u_voltage(i, drive);
series_node(i) = wd.series(i);
res_probe(i) = wd.resistor_Vout(i, 820);
res_load(i) = wd.resistor(i, 1800);

resistor_Vout_test = wd.buildtree(vsrc : (series_node : (res_probe, res_load)));
```
Note: the adaptor must be declared as a separate function before integration into the connection tree.
Correct implementation is shown above.
#### References
K. Werner, "Virtual Analog Modeling of Audio Circuitry Using Wave Digital Filters", 1.2.1

---

## wd.resistor_Iout

----------------------`(wd.)resistor_Iout`--------------------------
Resistor + current Out.
A basic adaptor implementing a resistor for use within Wave Digital Filter connection trees.
It should be used as a leaf/terminating element of the connection tree.
The resistor will also pass the current through itself as an output of the model.
#### Usage
```faust
rout(i) = resistor_Iout(i, R);
buildtree( A : rout ) : _
```
Where:
* `i`: index used by model-building functions. Should never be user declared.
* `R` : Resistance/Impedance of the resistor being modeled in Ohms.
#### Test
```faust
wd = library("wdmodels.lib");
os = library("oscillators.lib");

drive = os.osc(220);

vsrc(i) = wd.u_voltage(i, drive);
series_node(i) = wd.series(i);
current_probe(i) = wd.resistor_Iout(i, 1000);
load(i) = wd.resistor_Vout(i, 1500);

resistor_Iout_test = wd.buildtree(vsrc : (series_node : (current_probe, load)));
```
Note: the adaptor must be declared as a separate function before integration into the connection tree.
Correct implementation is shown above.
#### References
K. Werner, "Virtual Analog Modeling of Audio Circuitry Using Wave Digital Filters", 1.2.1

---

## wd.u_voltage

----------------------`(wd.)u_voltage`--------------------------
Unadapted Ideal Voltage Source.
An adaptor implementing an ideal voltage source within Wave Digital Filter connection trees.
It should be used as the root/top element of the connection tree.
Can be used for either DC (constant) or AC (signal) voltage sources.
#### Usage
```faust
v1(i) = u_Voltage(i, ein);
buildtree( v1 : B );
```
Where:
* `i`: index used by model-building functions. Should never be user declared.
* `ein` : Voltage/Potential across ideal voltage source in Volts
#### Test
```faust
wd = library("wdmodels.lib");
os = library("oscillators.lib");

drive = os.osc(330);

vsrc(i) = wd.u_voltage(i, drive);
series_node(i) = wd.series(i);
branch_a(i) = wd.resistor(i, 1200);
branch_b(i) = wd.resistor_Vout(i, 2200);

u_voltage_test = wd.buildtree(vsrc : (series_node : (branch_a, branch_b)));
```
Note: only usable as the root of a tree.
The adaptor must be declared as a separate function before integration into the connection tree.
Correct implementation is shown above.
#### References
K. Werner, "Virtual Analog Modeling of Audio Circuitry Using Wave Digital Filters", 1.2.2

---

## wd.u_current

----------------------`(wd.)u_current`--------------------------
Unadapted Ideal Current Source.
An unadapted adaptor implementing an ideal current source within Wave Digital Filter connection trees.
It should be used as the root/top element of the connection tree.
Can be used for either DC (constant) or AC (signal) current sources.
#### Usage
```faust
i1(i) = u_current(i, jin);
buildtree( i1 : B );
```
Where:
* `i`: index used by model-building functions. Should never be user declared.
* `jin` : Current through the ideal current source in Amps
#### Test
```faust
wd = library("wdmodels.lib");
os = library("oscillators.lib");

drive = os.osc(110);

isrc(i) = wd.u_current(i, drive);
parallel_node(i) = wd.parallel(i);
branch_a(i) = wd.resistor(i, 560);
branch_b(i) = wd.resistor_Vout(i, 2200);

u_current_test = wd.buildtree(isrc : (parallel_node : (branch_a, branch_b)));
```
Note: only usable as the root of a tree.
The adaptor must be declared as a separate function before integration into the connection tree.
Correct implementation is shown above.
#### References
K. Werner, "Virtual Analog Modeling of Audio Circuitry Using Wave Digital Filters", 1.2.3

---

## wd.resVoltage

----------------------`(wd.)resVoltage`--------------------------
Adapted Resistive Voltage Source.
An adaptor implementing a resistive voltage source within Wave Digital Filter connection trees.
It should be used as a leaf/terminating element of the connection tree.
It is comprised of an ideal voltage source in series with a resistor.
Can be used for either DC (constant) or AC (signal) voltage sources.
#### Usage
```faust
v1(i) = resVoltage(i, R, ein);
buildtree( A : v1 );
```
Where:
* `i`: index used by model-building functions. Should never be user declared
* `R` : Resistance/Impedance of the series resistor in Ohms
* `ein` : Voltage/Potential of the ideal voltage source in Volts
#### Test
```faust
wd = library("wdmodels.lib");
os = library("oscillators.lib");

drive = os.osc(440);

vsrc(i) = wd.u_voltage(i, drive);
series_node(i) = wd.series(i);
branch_source(i) = wd.resVoltage(i, 1000, 0.5);
probe(i) = wd.resistor_Vout(i, 1800);

resVoltage_test = wd.buildtree(vsrc : (series_node : (branch_source, probe)));
```
Note: the adaptor must be declared as a separate function before integration into the connection tree.
Correct implementation is shown above.
#### References
K. Werner, "Virtual Analog Modeling of Audio Circuitry Using Wave Digital Filters", 1.2.4

---

## wd.resVoltage_Vout

----------------------`(wd.)resVoltage_Vout`--------------------------
Adapted Resistive Voltage Source + voltage output.
An adaptor implementing an adapted resistive voltage source within Wave Digital Filter connection trees.
It should be used as a leaf/terminating element of the connection tree.
It is comprised of an ideal voltage source in series with a resistor.
Can be used for either DC (constant) or AC (signal) voltage sources.
The resistive voltage source will also pass the voltage across it as an output of the model.
#### Usage
```faust
vout(i) = resVoltage_Vout(i, R, ein);
buildtree( A : vout ) : _
```
Where:
* `i`: index used by model-building functions. Should never be user declared
* `R` : Resistance/Impedance of the series resistor in Ohms
* `ein` : Voltage/Potential across ideal voltage source in Volts
#### Test
```faust
wd = library("wdmodels.lib");
os = library("oscillators.lib");

drive = os.osc(330);

vsrc(i) = wd.u_voltage(i, drive);
series_node(i) = wd.series(i);
branch_source(i) = wd.resVoltage_Vout(i, 1500, 0.3);
load(i) = wd.resistor(i, 2200);

resVoltage_Vout_test = wd.buildtree(vsrc : (series_node : (branch_source, load)));
```
Note: the adaptor must be declared as a separate function before integration into the connection tree.
Correct implementation is shown above.
#### References
K. Werner, "Virtual Analog Modeling of Audio Circuitry Using Wave Digital Filters", 1.2.4

---

## wd.u_resVoltage

----------------------`(wd.)u_resVoltage`--------------------------
Unadapted Resistive Voltage Source.
An unadapted adaptor implementing a resistive voltage source within Wave Digital Filter connection trees.
It should be used as the root/top element of the connection tree.
It is comprised of an ideal voltage source in series with a resistor.
Can be used for either DC (constant) or AC (signal) voltage sources.
#### Usage
```faust
v1(i) = u_resVoltage(i, R, ein);
buildtree( v1 : B );
```
Where:
* `i`: index used by model-building functions. Should never be user declared
* `R` : Resistance/Impedance of the series resistor in Ohms
* `ein` : Voltage/Potential across ideal voltage source in Volts
#### Test
```faust
wd = library("wdmodels.lib");
os = library("oscillators.lib");

drive = os.osc(220);

root(i) = wd.u_resVoltage(i, 1800, drive);
series_node(i) = wd.series(i);
branch_a(i) = wd.resistor(i, 1500);
branch_b(i) = wd.resistor_Vout(i, 2200);

u_resVoltage_test = wd.buildtree(root : (series_node : (branch_a, branch_b)));
```
Note: only usable as the root of a tree.
The adaptor must be declared as a separate function before integration into the connection tree.
Correct implementation is shown above.
#### References
K. Werner, "Virtual Analog Modeling of Audio Circuitry Using Wave Digital Filters", 1.2.4

---

## wd.resCurrent

----------------------`(wd.)resCurrent`--------------------------
Adapted Resistive Current Source.
An adaptor implementing a resistive current source within Wave Digital Filter connection trees.
It should be used as a leaf/terminating element of the connection tree.
It is comprised of an ideal current source in parallel with a resistor.
Can be used for either DC (constant) or AC (signal) current sources.
#### Usage
```faust
i1(i) = resCurrent(i, R, jin);
buildtree( A : i1 );
```
Where:
* `i`: index used by model-building functions. Should never be user declared.
* `R` : Resistance/Impedance of the parallel resistor in Ohms
* `jin` : Current through the ideal current source in Amps
#### Test
```faust
wd = library("wdmodels.lib");
os = library("oscillators.lib");

drive = os.osc(110);

root(i) = wd.u_current(i, drive);
parallel_node(i) = wd.parallel(i);
source_branch(i) = wd.resCurrent(i, 2200, 0.15);
probe(i) = wd.resistor_Vout(i, 1500);

resCurrent_test = wd.buildtree(root : (parallel_node : (source_branch, probe)));
```
Note: the adaptor must be declared as a separate function before integration into the connection tree.
Correct implementation is shown above.
#### References
K. Werner, "Virtual Analog Modeling of Audio Circuitry Using Wave Digital Filters", 1.2.5

---

## wd.u_resCurrent

----------------------`(wd.)u_resCurrent`--------------------------
Unadapted Resistive Current Source.
An unadapted adaptor implementing a resistive current source within Wave Digital Filter connection trees.
It should be used as the root/top element of the connection tree.
It is comprised of an ideal current source in parallel with a resistor.
Can be used for either DC (constant) or AC (signal) current sources.
#### Usage
```faust
i1(i) = u_resCurrent(i, R, jin);
buildtree( i1 : B );
```
Where:
* `i`: index used by model-building functions. Should never be user declared.
* `R` : Resistance/Impedance of the series resistor in Ohms
* `jin` : Current through the ideal current source in Amps
#### Test
```faust
wd = library("wdmodels.lib");
os = library("oscillators.lib");

drive = os.osc(150);

root(i) = wd.u_resCurrent(i, 2000, drive);
parallel_node(i) = wd.parallel(i);
branch_a(i) = wd.resistor(i, 1200);
branch_b(i) = wd.resistor_Vout(i, 1800);

u_resCurrent_test = wd.buildtree(root : (parallel_node : (branch_a, branch_b)));
```
Note: only usable as the root of a tree.
The adaptor must be declared as a separate function before integration into the connection tree.
Correct implementation is shown above.
#### References
K. Werner, "Virtual Analog Modeling of Audio Circuitry Using Wave Digital Filters", 1.2.5

---

## wd.u_switch

----------------------`(wd.)u_switch`--------------------------
Unadapted Ideal Switch.
An unadapted adaptor implementing an ideal switch for Wave Digital Filter connection trees.
It should be used as the root/top element of the connection tree
#### Usage
```faust
s1(i) = u_resCurrent(i, lambda);
buildtree( s1 : B );
```
Where:
* `i`: index used by model-building functions. Should never be user declared.
* `lambda` : switch state control. -1 for closed switch, 1 for open switch.
#### Test
```faust
wd = library("wdmodels.lib");
os = library("oscillators.lib");

drive = os.osc(330);
lambda = hslider("u_switch:lambda", -1, -1, 1, 0.01);

root(i) = wd.u_switch(i, lambda);
series_node(i) = wd.series(i);
branch_a(i) = wd.resistor(i, 1000);
branch_b(i) = wd.resistor_Vout(i, 2200);

u_switch_test = wd.buildtree(root : (series_node : (branch_a, branch_b)));
```
Note: only usable as the root of a tree.
The adaptor must be declared as a separate function before integration into the connection tree.
Correct implementation is shown above.
#### References
K. Werner, "Virtual Analog Modeling of Audio Circuitry Using Wave Digital Filters", 1.2.8

---

## wd.capacitor

----------------------`(wd.)capacitor`--------------------------
Adapted Capacitor.
A basic adaptor implementing a capacitor for use within Wave Digital Filter connection trees.
It should be used as a leaf/terminating element of the connection tree.
This capacitor model was digitized using the bi-linear transform.
#### Usage
```faust
c1(i) = capacitor(i, R);
buildtree( A : c1 ) : _
```
Where:
* `i`: index used by model-building functions. Should never be user declared.
* `R` : Capacitance/Impedance of the capacitor being modeled in Farads.
#### Test
```faust
wd = library("wdmodels.lib");
os = library("oscillators.lib");

drive = os.osc(440);

vsrc(i) = wd.u_voltage(i, drive);
series_node(i) = wd.series(i);
cap_branch(i) = wd.capacitor(i, 1e-7);
probe(i) = wd.resistor_Vout(i, 1800);

capacitor_test = wd.buildtree(vsrc : (series_node : (cap_branch, probe)));
```
Note: the adaptor must be declared as a separate function before integration into the connection tree.
Correct implementation is shown above.
#### References
K. Werner, "Virtual Analog Modeling of Audio Circuitry Using Wave Digital Filters", 1.3.1

---

## wd.capacitor_Vout

----------------------`(wd.)capacitor_Vout`--------------------------
Adapted Capacitor + voltage out.
A basic adaptor implementing a capacitor for use within Wave Digital Filter connection trees.
It should be used as a leaf/terminating element of the connection tree.
The capacitor will also pass the voltage across itself as an output of the model.
This capacitor model was digitized using the bi-linear transform.
#### Usage
```faust
cout(i) = capacitor_Vout(i, R);
buildtree( A : cout ) : _
```
Where:
* `i`: index used by model-building functions. Should never be user declared
* `R` : Capacitance/Impedence of the capacitor being modeled in Farads
#### Test
```faust
wd = library("wdmodels.lib");
os = library("oscillators.lib");

drive = os.osc(330);

vsrc(i) = wd.u_voltage(i, drive);
series_node(i) = wd.series(i);
cap_branch(i) = wd.capacitor_Vout(i, 2e-7);
load(i) = wd.resistor(i, 1500);

capacitor_Vout_test = wd.buildtree(vsrc : (series_node : (cap_branch, load)));
```
Note: the adaptor must be declared as a seperate function before integration into the connection tree.
Correct implementation is shown above.
#### References
K. Werner, "Virtual Analog Modeling of Audio Circuitry Using Wave Digital Filters", 1.3.1

---

## wd.inductor

----------------------`(wd.)inductor`--------------------------
Unadapted Inductor.
A basic adaptor implementing an inductor for use within Wave Digital Filter connection trees.
It should be used as a leaf/terminating element of the connection tree.
This inductor model was digitized using the bi-linear transform.
#### Usage
```faust
l1(i) = inductor(i, R);
buildtree( A : l1 );
```
Where:
* `i`: index used by model-building functions. Should never be user declared
* `R` : Inductance/Impedance of the inductor being modeled in Henries
#### Test
```faust
wd = library("wdmodels.lib");
os = library("oscillators.lib");

drive = os.osc(260);

vsrc(i) = wd.u_voltage(i, drive);
series_node(i) = wd.series(i);
inductive_branch(i) = wd.inductor(i, 0.01);
probe(i) = wd.resistor_Vout(i, 2200);

inductor_test = wd.buildtree(vsrc : (series_node : (inductive_branch, probe)));
```
Note: the adaptor must be declared as a separate function before integration into the connection tree.
Correct implementation is shown above.
#### References
K. Werner, "Virtual Analog Modeling of Audio Circuitry Using Wave Digital Filters", 1.3.2

---

## wd.inductor_Vout

----------------------`(wd.)inductor_Vout`--------------------------
Unadapted Inductor + Voltage out.
A basic adaptor implementing an inductor for use within Wave Digital Filter connection trees.
It should be used as a leaf/terminating element of the connection tree.
The inductor will also pass the voltage across itself as an output of the model.
This inductor model was digitized using the bi-linear transform.
#### Usage
```faust
lout(i) = inductor_Vout(i, R);
buildtree( A : lout ) : _
```
Where:
* `i`: index used by model-building functions. Should never be user declared
* `R` : Inductance/Impedance of the inductor being modeled in Henries
#### Test
```faust
wd = library("wdmodels.lib");
os = library("oscillators.lib");

drive = os.osc(280);

vsrc(i) = wd.u_voltage(i, drive);
series_node(i) = wd.series(i);
inductive_branch(i) = wd.inductor_Vout(i, 0.02);
load(i) = wd.resistor(i, 1500);

inductor_Vout_test = wd.buildtree(vsrc : (series_node : (inductive_branch, load)));
```
Note: the adaptor must be declared as a separate function before integration into the connection tree.
Correct implementation is shown above.
#### References
K. Werner, "Virtual Analog Modeling of Audio Circuitry Using Wave Digital Filters", 1.3.2

---

## wd.u_idealDiode

----------------------`(wd.)u_idealDiode`--------------------------
Unadapted Ideal Diode.
An unadapted adaptor implementing an ideal diode for Wave Digital Filter connection trees.
It should be used as the root/top element of the connection tree.
#### Usage
```faust
buildtree( u_idealDiode : B );
```
Note: only usable as the root of a tree.
Correct implementation is shown above.
#### Test
```faust
wd = library("wdmodels.lib");
os = library("oscillators.lib");

diode(i) = wd.u_idealDiode(i);
series_node(i) = wd.series(i);
branch_a(i) = wd.resistor(i, 1200);
branch_b(i) = wd.resistor_Vout(i, 1800);

u_idealDiode_test = wd.buildtree(diode : (series_node : (branch_a, branch_b)));
```
#### References
K. Werner, "Virtual Analog Modeling of Audio Circuitry Using Wave Digital Filters", 3.2.3

---

## wd.u_chua

----------------------`(wd.)u_chua`--------------------------
Unadapted Chua Diode.
An adaptor implementing the chua diode / non-linear resistor within Wave Digital Filter connection trees.
It should be used as the root/top element of the connection tree.
#### Usage
```faust
chua1(i) = u_chua(i, G1, G2, V0);
buildtree( chua1 : B );
```
Where:
* `i`: index used by model-building functions. Should never be user declared
* `G1` : resistance parameter 1 of the chua diode
* `G2` : resistance parameter 2 of the chua diode
* `V0` : voltage parameter of the chua diode
#### Test
```faust
wd = library("wdmodels.lib");
os = library("oscillators.lib");

chua_node(i) = wd.u_chua(i, 1e-3, 5e-4, 0.2);
series_node(i) = wd.series(i);
branch_a(i) = wd.resistor(i, 1500);
branch_b(i) = wd.resistor_Vout(i, 2200);

u_chua_test = wd.buildtree(chua_node : (series_node : (branch_a, branch_b)));
```
Note: only usable as the root of a tree.
The adaptor must be declared as a separate function before integration into the connection tree.
Correct implementation is shown above.
#### References
Meerkotter and Scholz, "Digital Simulation of Nonlinear Circuits by Wave Digital Filter Principles"

---

## wd.lambert

----------------------`(wd.)lambert`--------------------------
An implementation of the lambert function.
It uses Halley's method of iteration to approximate the output.
Included in the WD library for use in non-linear diode models.
Adapted from K M Brigg's c++ lambert function approximation.
#### Usage
```faust
lambert(n, itr) : _
```
Where:
* `n`: value at which the lambert function will be evaluated
* `itr`: number of iterations before output
#### Test
```faust
wd = library("wdmodels.lib");
os = library("oscillators.lib");

lambert_gain = wd.lambert(0.5, 6);
lambert_test = os.osc(220) * lambert_gain;
```

---

## wd.u_diodePair

----------------------`(wd.)u_diodePair`--------------------------
Unadapted pair of diodes facing in opposite directions.
An unadapted adaptor implementing two antiparallel diodes for Wave Digital Filter connection trees.
The behavior is approximated using Schottkey's ideal diode law.
#### Usage
```faust
d1(i) = u_diodePair(i, Is, Vt);
buildtree( d1 : B );
```
Where:
* `i`: index used by model-building functions. Should never be user declared
* `Is` : saturation current of the diodes
* `Vt` : thermal resistances of the diodes
#### Test
```faust
wd = library("wdmodels.lib");

u_diodePair_test = wd.u_diodePair(2, 1e-12, 0.025);
```
Note: only usable as the root of a tree.
Correct implementation is shown above.
#### References
K. Werner et al. "An Improved and Generalized Diode Clipper Model for Wave Digital Filters"

---

## wd.u_diodeSingle

----------------------`(wd.)u_diodeSingle`--------------------------
Unadapted single diode.
An unadapted adaptor implementing a single diode for Wave Digital Filter connection trees.
The behavior is approximated using Schottkey's ideal diode law.
#### Usage
```faust
d1(i) = u_diodeSingle(i, Is, Vt);
buildtree( d1 : B );
```
Where:
* `i`: index used by model-building functions. Should never be user declared
* `Is` : saturation current of the diodes
* `Vt` : thermal resistances of the diodes
#### Test
```faust
wd = library("wdmodels.lib");

u_diodeSingle_test = wd.u_diodeSingle(2, 8e-13, 0.026);
```
Note: only usable as the root of a tree.
Correct implementation is shown above.
#### References
K. Werner et al. "An Improved and Generalized Diode Clipper Model for Wave Digital Filters"

---

## wd.u_diodeAntiparallel

----------------------`(wd.)u_diodeAntiparallel`--------------------------
Unadapted set of antiparallel diodes with M diodes facing forwards and N diodes facing backwards.
An unadapted adaptor implementing antiparallel diodes for Wave Digital Filter connection trees.
The behavior is approximated using Schottkey's ideal diode law.
#### Usage
```faust
d1(i) = u_diodeAntiparallel(i, Is, Vt);
buildtree( d1 : B );
```
Where:
* `i`: index used by model-building functions. Should never be user declared
* `Is` : saturation current of the diodes
* `Vt` : thermal resistances of the diodes
#### Test
```faust
wd = library("wdmodels.lib");
u_diodeAntiparallel_test = wd.u_diodeAntiparallel(2, 1e-12, 0.025, 2, 2);
```
Note: only usable as the root of a tree.
Correct implementation is shown above.
#### References
K. Werner et al. "An Improved and Generalized Diode Clipper Model for Wave Digital Filters"

---

## wd.u_parallel2Port

----------------------`(wd.)u_parallel2Port`--------------------------
Unadapted 2-port parallel connection.
An unadapted adaptor implementing a 2-port parallel connection between adaptors for Wave Digital Filter connection trees.
Elements connected to this adaptor will behave as if connected in parallel in circuit.
#### Usage
```faust
buildtree( u_parallel2Port : (A, B) );
```
Note: only usable as the root of a tree.
This adaptor has no user-accessible parameters.
Correct implementation is shown above.
#### Test
```faust
wd = library("wdmodels.lib");
os = library("oscillators.lib");

root(i) = wd.u_parallel2Port(i);
branch_source(i) = wd.resVoltage_Vout(i, 1500, 0.2 * os.osc(220));
branch_load(i) = wd.resistor(i, 1800);

u_parallel2Port_test = wd.buildtree(root : (branch_source, branch_load));
```
#### References
K. Werner, "Virtual Analog Modeling of Audio Circuitry Using Wave Digital Filters", 1.4.1

---

## wd.parallel2Port

----------------------`(wd.)parallel2Port`--------------------------
Adapted 2-port parallel connection.
An adaptor implementing a 2-port parallel connection between adaptors for Wave Digital Filter connection trees.
Elements connected to this adaptor will behave as if connected in parallel in circuit.
#### Usage
```faust
buildtree( A : parallel2Port : B );
```
Note: this adaptor has no user-accessible parameters.
It should be used within the connection tree with one previous and one forward adaptor.
Correct implementation is shown above.
#### Test
```faust
wd = library("wdmodels.lib");
os = library("oscillators.lib");

vsrc(i) = wd.u_voltage(i, os.osc(260));
connector(i) = wd.parallel2Port(i);
load(i) = wd.resistor_Vout(i, 1800);

parallel2Port_test = wd.buildtree(vsrc : (connector : load));
```
#### References
K. Werner, "Virtual Analog Modeling of Audio Circuitry Using Wave Digital Filters", 1.4.1

---

## wd.u_series2Port

----------------------`(wd.)u_series2Port`--------------------------
Unadapted 2-port series connection.
An unadapted adaptor implementing a 2-port series connection between adaptors for Wave Digital Filter connection trees.
Elements connected to this adaptor will behave as if connected in series in circuit.
#### Usage
```faust
buildtree( u_series2Port : (A, B) );
```
Note: only usable as the root of a tree.
This adaptor has no user-accessible parameters.
Correct implementation is shown above.
#### Test
```faust
wd = library("wdmodels.lib");
os = library("oscillators.lib");

root(i) = wd.u_series2Port(i);
branch_source(i) = wd.resVoltage_Vout(i, 1200, 0.25 * os.osc(180));
branch_load(i) = wd.resistor(i, 1800);

u_series2Port_test = wd.buildtree(root : (branch_source, branch_load));
```
#### References
K. Werner, "Virtual Analog Modeling of Audio Circuitry Using Wave Digital Filters", 1.4.1

---

## wd.series2Port

----------------------`(wd.)series2Port`--------------------------
Adapted 2-port series connection.
An adaptor implementing a 2-port series connection between adaptors for Wave Digital Filter connection trees.
Elements connected to this adaptor will behave as if connected in series in circuit.
#### Usage
```faust
buildtree( A : series2Port : B );
```
Note: this adaptor has no user-accessible parameters.
It should be used within the connection tree with one previous and one forward adaptor.
Correct implementation is shown above.
#### Test
```faust
wd = library("wdmodels.lib");
os = library("oscillators.lib");

vsrc(i) = wd.u_voltage(i, os.osc(200));
connector(i) = wd.series2Port(i);
load(i) = wd.resistor_Vout(i, 2200);

series2Port_test = wd.buildtree(vsrc : (connector : load));
```
#### References
K. Werner, "Virtual Analog Modeling of Audio Circuitry Using Wave Digital Filters", 1.4.1

---

## wd.parallelCurrent

----------------------`(wd.)parallelCurrent`--------------------------
Adapted 2-port parallel connection + ideal current source.
An adaptor implementing a 2-port series connection and internal idealized current source between adaptors for Wave Digital Filter connection trees.
This adaptor connects the two connected elements and an additional ideal current source in parallel.
#### Usage
```faust
i1(i) = parallelCurrent(i, jin);
buildtree(A : i1 : B);
```
Where:
* `i`: index used by model-building functions. Should never be user declared
* `jin` :  Current through the ideal current source in Amps
#### Test
```faust
wd = library("wdmodels.lib");
os = library("oscillators.lib");

vsrc(i) = wd.u_voltage(i, os.osc(240));
connector(i) = wd.parallelCurrent(i, 0.1);
load(i) = wd.resistor_Vout(i, 1500);

parallelCurrent_test = wd.buildtree(vsrc : (connector : load));
```
Note: the adaptor must be declared as a separate function before integration into the connection tree.
It should be used within a connection tree with one previous and one forward adaptor.
Correct implementation is shown above.
#### References
K. Werner, "Virtual Analog Modeling of Audio Circuitry Using Wave Digital Filters", 1.4.2

---

## wd.seriesVoltage

----------------------`(wd.)seriesVoltage`--------------------------
Adapted 2-port series connection + ideal voltage source.
An adaptor implementing a 2-port series connection and internal ideal voltage source between adaptors for Wave Digital Filter connection trees.
This adaptor connects the two connected adaptors and an additional ideal voltage source in series.
#### Usage
```faust
v1(i) = seriesVoltage(i, vin)
buildtree( A : v1 : B );
```
Where:
* `i`: index used by model-building functions. Should never be user declared
* `vin` :  voltage across the ideal current source in Volts
#### Test
```faust
wd = library("wdmodels.lib");
os = library("oscillators.lib");

vsrc(i) = wd.u_voltage(i, os.osc(210));
connector(i) = wd.seriesVoltage(i, 0.3);
load(i) = wd.resistor_Vout(i, 1500);

seriesVoltage_test = wd.buildtree(vsrc : (connector : load));
```
Note: the adaptor must be declared as a separate function before integration into the connection tree.
It should be used within the connection tree with one previous and one forward adaptor.
#### References
K. Werner, "Virtual Analog Modeling of Audio Circuitry Using Wave Digital Filters", 1.4.2

---

## wd.u_transformer

----------------------`(wd.)u_transformer`--------------------------
Unadapted ideal transformer.
An adaptor implementing an ideal transformer for Wave Digital Filter connection trees.
The first downward-facing port corresponds to the primary winding connections, and the second downward-facing port to the secondary winding connections.
#### Usage
```faust
t1(i) = u_transformer(i, tr);
buildtree(t1 : (A , B));
```
Where:
* `i`: index used by model-building functions. Should never be user declared
* `tr` :  the turn ratio between the windings on the primary and secondary coils
#### Test
```faust
wd = library("wdmodels.lib");
os = library("oscillators.lib");

root(i) = wd.u_transformer(i, 2.0);
primary(i) = wd.resVoltage_Vout(i, 1500, 0.2 * os.osc(220));
secondary(i) = wd.resistor_Vout(i, 2200);

u_transformer_test = wd.buildtree(root : (primary, secondary));
```
Note: the adaptor must be declared as a separate function before integration into the connection tree.
It may only be used as the root of the connection tree with two forward nodes.
#### References
K. Werner, "Virtual Analog Modeling of Audio Circuitry Using Wave Digital Filters", 1.4.3

---

## wd.transformer

----------------------`(wd.)transformer`--------------------------
Adapted ideal transformer.
An adaptor implementing an ideal transformer for Wave Digital Filter connection trees.
The upward-facing port corresponds to the primary winding connections, and the downward-facing port to the secondary winding connections
#### Usage
```faust
t1(i) = transformer(i, tr);
buildtree(A : t1 : B);
```
Where:
* `i`: index used by model-building functions. Should never be user declared
* `tr` :  the turn ratio between the windings on the primary and secondary coils
#### Test
```faust
wd = library("wdmodels.lib");
os = library("oscillators.lib");

vsrc(i) = wd.u_voltage(i, os.osc(180));
xfmr(i) = wd.transformer(i, 2.5);
load(i) = wd.resistor_Vout(i, 2200);

transformer_test = wd.buildtree(vsrc : (xfmr : load));
```
Note: the adaptor must be declared as a separate function before integration into the connection tree.
It should be used within the connection tree with one backward and one forward nodes.
#### References
K. Werner, "Virtual Analog Modeling of Audio Circuitry Using Wave Digital Filters", 1.4.3

---

## wd.u_transformerActive

----------------------`(wd.)u_transformerActive`--------------------------
Unadapted ideal active transformer.
An adaptor implementing an ideal transformer for Wave Digital Filter connection trees.
The first downward-facing port corresponds to the primary winding connections, and the second downward-facing port to the secondary winding connections.
#### Usage
```faust
t1(i) = u_transformerActive(i, gamma1, gamma2);
buildtree(t1 : (A , B));
```
Where:
* `i`: index used by model-building functions. Should never be user declared
* `gamma1` :  the turn ratio describing the voltage relationship between the primary and secondary coils
* `gamma2` :  the turn ratio describing the current relationship between the primary and secondary coils
#### Test
```faust
wd = library("wdmodels.lib");
os = library("oscillators.lib");

root(i) = wd.u_transformerActive(i, 0.9, 0.8);
primary(i) = wd.resVoltage_Vout(i, 1200, 0.18 * os.osc(190));
secondary(i) = wd.resistor_Vout(i, 2200);

u_transformerActive_test = wd.buildtree(root : (primary, secondary));
```
Note: the adaptor must be declared as a separate function before integration into the connection tree.
It may only be used as the root of the connection tree with two forward nodes.
#### References
K. Werner, "Virtual Analog Modeling of Audio Circuitry Using Wave Digital Filters", 1.4.3

---

## wd.transformerActive

----------------------`(wd.)transformerActive`--------------------------
Adapted ideal active transformer.
An adaptor implementing an ideal active transformer for Wave Digital Filter connection trees.
The upward-facing port corresponds to the primary winding connections, and the downward-facing port to the secondary winding connections
#### Usage
```faust
t1(i) = transformerActive(i, gamma1, gamma2);
buildtree(A : t1 : B);
```
Where:
* `i`: index used by model-building functions. Should never be user declared
* `gamma1` :  the turn ratio describing the voltage relationship between the primary and secondary coils
* `gamma2` :  the turn ratio describing the current relationship between the primary and secondary coils
#### Test
```faust
wd = library("wdmodels.lib");
os = library("oscillators.lib");

vsrc(i) = wd.u_voltage(i, os.osc(175));
xfmr(i) = wd.transformerActive(i, 0.9, 0.8);
load(i) = wd.resistor_Vout(i, 2200);

transformerActive_test = wd.buildtree(vsrc : (xfmr : load));
```
Note: the adaptor must be declared as a separate function before integration into the connection tree.
It should be used within the connection tree with two forward nodes.
#### References
K. Werner, "Virtual Analog Modeling of Audio Circuitry Using Wave Digital Filters", 1.4.3

---

## wd.parallel

----------------------`(wd.)parallel`--------------------------
Adapted 3-port parallel connection.
An adaptor implementing a 3-port parallel connection between adaptors for Wave Digital Filter connection trees.
This adaptor is used to connect adaptors simulating components connected in parallel in the circuit.
#### Usage
```faust
buildtree( A : parallel : (B, C) );
```
Note: this adaptor has no user-accessible parameters.
It should be used within the connection tree with one previous and two forward adaptors.
#### Test
```faust
wd = library("wdmodels.lib");
os = library("oscillators.lib");

vsrc(i) = wd.u_voltage(i, os.osc(220));
junction(i) = wd.parallel(i);
branch_a(i) = wd.resistor(i, 1200);
branch_b(i) = wd.resistor_Vout(i, 1800);

parallel_test = wd.buildtree(vsrc : (junction : (branch_a, branch_b)));
```
#### References
K. Werner, "Virtual Analog Modeling of Audio Circuitry Using Wave Digital Filters", 1.5.1

---

## wd.series

----------------------`(wd.)series`--------------------------
Adapted 3-port series connection.
An adaptor implementing a 3-port series connection between adaptors for Wave Digital Filter connection trees.
This adaptor is used to connect adaptors simulating components connected in series in the circuit.
#### Usage
```faust

tree = A : (series : (B, C));
```
Note: this adaptor has no user-accessible parameters.
It should be used within the connection tree with one previous and two forward adaptors.
#### Test
```faust
wd = library("wdmodels.lib");
os = library("oscillators.lib");

vsrc(i) = wd.u_voltage(i, os.osc(260));
junction(i) = wd.series(i);
branch_a(i) = wd.resistor(i, 1000);
branch_b(i) = wd.resistor_Vout(i, 2200);

series_test = wd.buildtree(vsrc : (junction : (branch_a, branch_b)));
```
#### References
K. Werner, "Virtual Analog Modeling of Audio Circuitry Using Wave Digital Filters", 1.5.2

---

## wd.u_sixportPassive

----------------------`(wd.)u_sixportPassive`--------------------------
Unadapted six-port rigid connection.
An adaptor implementing a six-port passive rigid connection between elements.
It implements the simplest possible rigid connection found in the Fender Bassman Tonestack circuit.
#### Usage
```faust

tree = u_sixportPassive : (A, B, C, D, E, F));
```
Note: this adaptor has no user-accessible parameters.
It should be used within the connection tree with six forward adaptors.
#### Test
```faust
wd = library("wdmodels.lib");
os = library("oscillators.lib");

u_sixportPassive_test = (1000, 1200, 1400, 1600, 1800, 2000, os.osc(220), 0, 0, 0, 0, 0, 0)
: wd.u_sixportPassive(0) : _, !, !, !, !;
```
#### References
K. Werner, "Virtual Analog Modeling of Audio Circuitry Using Wave Digital Filters", 2.1.5

---

## wd.genericNode

----------------------`(wd.)genericNode`--------------------------
Function for generating an adapted node from another faust function or scattering matrix.
This function generates a node which is suitable for use in the connection tree structure.
`genericNode` separates the function that it is passed into upward-going and downward-going waves.
#### Usage
```faust
n1(i) = genericNode(i, scatter, upRes);
```
Where:
* `i`: index used by model-building functions. Should never be user declared
* `scatter` : the function which describes the the node's scattering behavior
* `upRes` : the function which describes the node's upward-facing port-resistance
#### Test
```faust
wd = library("wdmodels.lib");
os = library("oscillators.lib");

scatter(a) = -a * 0.3;
upRes = 1400;

node_iout(i) = wd.genericNode_Iout(i, scatter, upRes);
vsrc(i) = wd.u_voltage(i, os.osc(230));
branch(i) = wd.series(i);
load(i) = wd.resistor(i, 1800);

genericNode_Iout_test = wd.buildtree(vsrc : (branch : (node_iout, load)));
```
#### Test
```faust
wd = library("wdmodels.lib");
os = library("oscillators.lib");

scatter(a) = -a * 0.4;
upRes = 1600;

node_vout(i) = wd.genericNode_Vout(i, scatter, upRes);
vsrc(i) = wd.u_voltage(i, os.osc(200));
branch(i) = wd.series(i);
load(i) = wd.resistor(i, 1800);

genericNode_Vout_test = wd.buildtree(vsrc : (branch : (node_vout, load)));
```
#### Test
```faust
wd = library("wdmodels.lib");
os = library("oscillators.lib");

scatter(a) = -a * 0.5;
upRes = 1200;

node(i) = wd.genericNode(i, scatter, upRes);
vsrc(i) = wd.u_voltage(i, os.osc(220));
branch(i) = wd.series(i);
probe(i) = wd.resistor_Vout(i, 1800);

genericNode_test = wd.buildtree(vsrc : (branch : (node, probe)));
```
Note: `scatter` must be a function with n inputs, n outputs, and n-1 parameter inputs.
input/output 1 will be used as the adapted upward-facing port of the node, ports 2 to n will all be downward-facing.
The first input/output pair is assumed to already be adapted - i.e. the output 1 is not dependent on input 1.
The parameter inputs will receive the port resistances of the downward-facing ports.
`upRes` must be a function with n-1 parameter inputs and 1 output.
The parameter inputs will receive the port resistances of the downward-facing ports.
The output should give the upward-facing port resistance of the node based on the upward-facing port resistances of the input.
If used on a leaf element (n=1), the model will automatically introduce a one-sample delay.
Thus, the output of the node at sample t based on the input, a[t], should be the output one sample ahead, b[t+1].
This may require transformation of the output signal.

---

## wd.genericNode_Vout

----------------------`(wd.)genericNode_Vout`--------------------------
Function for generating a terminating/leaf node which gives the voltage across itself as a model output.
This function generates a node which is suitable for use in the connection tree structure.
It also calculates the voltage across the element and gives it as a model output.
#### Usage
```faust
n1(i) = genericNode_Vout(i, scatter, upRes);
```
Where:
* `i`: index used by model-building functions. Should never be user declared
* `scatter` : the function which describes the the node's scattering behavior
* `upRes` : the function which describes the node's upward-facing port-resistance
Note: `scatter` must be a function with 1 input and 1 output.
It should give the output from the node based on the incident wave.
The model will automatically introduce a one-sample delay to the output of the function
Thus, the output of the node at sample t based on the input, a[t], should be the output one sample ahead, b[t+1].
This may require transformation of the output signal.
`upRes` must be a function with no inputs and 1 output.
The output should give the upward-facing port resistance of the node.

---

## wd.genericNode_Iout

----------------------`(wd.)genericNode_Iout`--------------------------
Function for generating a terminating/leaf node which gives the current through itself as a model output.
This function generates a node which is suitable for use in the connection tree structure.
It also calculates the current through the element and gives it as a model output.
#### Usage
```faust
n1(i) = genericNode_Iout(i, scatter, upRes);
```
Where:
* `i`: index used by model-building functions. Should never be user declared
* `scatter` : the function which describes the the node's scattering behavior
* `upRes` : the function which describes the node's upward-facing port-resistance
Note: `scatter` must be a function with 1 input and 1 output.
It should give the output from the node based on the incident wave.
The model will automatically introduce a one-sample delay to the output of the function.
Thus, the output of the node at sample t based on the input, a[t], should be the output one sample ahead, b[t+1].
This may require transformation of the output signal.
`upRes` must be a function with no inputs and 1 output.
The output should give the upward-facing port resistance of the node.

---

## wd.u_genericNode

----------------------`(wd.)u_genericNode`--------------------------
Function for generating an unadapted node from another Faust function or scattering matrix.
This function generates a node which is suitable for use as the root of the connection tree structure.
#### Usage
```faust
n1(i) = u_genericNode(i, scatter);
```
Where:
* `i`: index used by model-building functions. Should never be user declared
* `scatter` : the function which describes the the node's scattering behavior
#### Test
```faust
wd = library("wdmodels.lib");
os = library("oscillators.lib");

scatter(a) = -a * 0.5;

root(i) = wd.u_genericNode(i, scatter);
branch(i) = wd.series(i);
load_a(i) = wd.resistor(i, 1500);
load_b(i) = wd.resistor_Vout(i, 2200);

u_genericNode_test = wd.buildtree(root : (branch : (load_a, load_b)));
```
Note:
`scatter` must be a function with n inputs, n outputs, and n parameter inputs.
each input/output pair will be used as a downward-facing port of the node
the parameter inputs will receive the port resistances of the downward-facing ports.

---

## wd.builddown

----------------------`(wd.)builddown`--------------------------
Function for building the structure for calculating waves traveling down the WD connection tree.
It recursively steps through the given tree, parametrizes the adaptors, and builds an algorithm.
It is used in conjunction with the buildup() function to create a model.
#### Usage
```faust
builddown(A : B)~buildup(A : B);
```
Where:
`(A : B)` : is a connection tree composed of WD adaptors
#### Test
```faust
wd = library("wdmodels.lib");
os = library("oscillators.lib");

vsrc(i) = wd.u_voltage(i, os.osc(220));
branch(i) = wd.series(i);
res_leaf(i) = wd.resistor(i, 1200);
probe(i) = wd.resistor_Vout(i, 1800);
tree = vsrc : (branch : (res_leaf, probe));

builddown_test = wd.builddown(tree) ~ wd.buildup(tree) : wd.buildout(tree);
```

---

## wd.buildup

----------------------`(wd.)buildup`--------------------------
Function for building the structure for calculating waves traveling up the WD connection tree.
It recursively steps through the given tree, parametrizes the adaptors, and builds an algorithm.
It is used in conjunction with the builddown() function to create a full structure.
#### Usage
```faust
builddown(A : B)~buildup(A : B);
```
Where:
`(A : B)` : is a connection tree composed of WD adaptors
#### Test
```faust
wd = library("wdmodels.lib");
os = library("oscillators.lib");

vsrc(i) = wd.u_voltage(i, os.osc(220));
branch(i) = wd.series(i);
res_leaf(i) = wd.resistor(i, 1200);
probe(i) = wd.resistor_Vout(i, 1800);
tree = vsrc : (branch : (res_leaf, probe));

buildup_test = wd.builddown(tree) ~ wd.buildup(tree) : wd.buildout(tree);
```

---

## wd.getres

----------------------`(wd.)getres`--------------------------
Function for determining the upward-facing port resistance of a partial WD connection tree.
It recursively steps through the given tree, parametrizes the adaptors, and builds an algorithm.
It is used by the buildup and builddown functions but is also helpful in testing.
#### Usage
```faust
getres(A : B)~getres(A : B);
```
Where:
`(A : B)` : is a partial connection tree composed of WD adaptors
#### Test
```faust
wd = library("wdmodels.lib");
os = library("oscillators.lib");

branch(i) = wd.series(i);
res_leaf(i) = wd.resistor(i, 1200);
probe(i) = wd.resistor_Vout(i, 1800);
subtree = branch : (res_leaf, probe);

getres_value = wd.getres(subtree);
getres_test = os.osc(110) * (1.0/(1.0 + getres_value));
```
Note:
This function cannot be used on a complete WD tree. When called on an unadapted adaptor (u_ prefix), it will create errors.

---

## wd.parres

----------------------`(wd.)parres`--------------------------
Function for determining the upward-facing port resistance of a partial WD connection tree.
It recursively steps through the given tree, parametrizes the adaptors, and builds an algorithm.
It is used by the buildup and builddown functions but is also helpful in testing.
This function is a parallelized version of `getres`.
#### Usage
```faust
parres((A , B))~parres((A , B));
```
Where:
`(A , B)` : is a partial connection tree composed of WD adaptors
#### Test
```faust
wd = library("wdmodels.lib");
os = library("oscillators.lib");

branchLeft(i) = wd.series(i);
res_left(i) = wd.resistor(i, 1200);
probe_left(i) = wd.resistor(i, 1800);
subtree_left = branchLeft : (res_left, probe_left);

branchRight(i) = wd.parallel(i);
res_right(i) = wd.resistor(i, 1500);
probe_right(i) = wd.resistor(i, 2200);
subtree_right = branchRight : (res_right, probe_right);

parres_test = wd.parres((subtree_left, subtree_right)) : _, !;
```
Note: this function cannot be used on a complete WD tree. When called on an unadapted adaptor (u_ prefix), it will create errors.

---

## wd.buildout

----------------------`(wd.)buildout`--------------------------
Function for creating the output matrix for a WD model from a WD connection tree.
It recursively steps through the given tree and creates an output matrix passing only outputs.
#### Usage
```faust
buildout( A : B );
```
Where:
`(A : B)` : is a connection tree composed of WD adaptors
#### Test
```faust
wd = library("wdmodels.lib");
os = library("oscillators.lib");

vsrc(i) = wd.u_voltage(i, os.osc(240));
branch(i) = wd.series(i);
res_leaf(i) = wd.resistor(i, 1200);
probe(i) = wd.resistor_Vout(i, 1800);
tree = vsrc : (branch : (res_leaf, probe));

buildout_matrix = wd.buildout(tree);
buildout_test = wd.builddown(tree) ~ wd.buildup(tree) : buildout_matrix;
```

---

## wd.buildtree

----------------------`(wd.)buildtree`--------------------------
Function for building the DSP model from a WD connection tree structure.
It recursively steps through the given tree, parametrizes the adaptors, and builds the algorithm.
#### Usage
```faust
buildtree(A : B);
```
Where:
`(A : B)` : a connection tree composed of WD adaptors
#### Test
```faust
wd = library("wdmodels.lib");
os = library("oscillators.lib");

vsrc(i) = wd.u_voltage(i, os.osc(220));
branch(i) = wd.series(i);
res_leaf(i) = wd.resistor(i, 1200);
probe(i) = wd.resistor_Vout(i, 1800);
tree = vsrc : (branch : (res_leaf, probe));

buildtree_test = wd.buildtree(tree);
```

---

# webaudio.lib
**Prefix:** `wa`

#################################### webaudio.lib ########################################
An implementation of the WebAudio API filters (https://www.w3.org/TR/webaudio/). Its official prefix is `wa`.

This library implement WebAudio filters, using their C++ version as a starting point,
taken from Mozilla Firefox implementation.

#### References

* <https://github.com/grame-cncm/faustlibraries/blob/master/webaudio.lib>
########################################################################################

## wa.lowpass2

--------------`(wa.)lowpass2`--------------
Standard second-order resonant lowpass filter with 12dB/octave rolloff.
Frequencies below the cutoff pass through, frequencies above it are attenuated.
#### Usage
```faust
_ : lowpass2(f0, Q, dtune) : _
```
Where:
* `f0`: cutoff frequency in Hz
* `Q`: the quality factor
* `dtune`: detuning of the frequency in cents
#### Test
```faust
wa = library("webaudio.lib");
os = library("oscillators.lib");
lowpass2_test = os.osc(440) : wa.lowpass2(1000, 0.707, 0);
```
#### References
* <https://searchfox.org/mozilla-central/source/dom/media/webaudio/blink/Biquad.cpp#98>

---

## wa.highpass2

--------------`(wa.)highpass2`--------------
Standard second-order resonant highpass filter with 12dB/octave rolloff.
Frequencies below the cutoff are attenuated, frequencies above it pass through.
#### Usage
```faust
_ : highpass2(f0, Q, dtune) : _
```
Where:
* `f0`: cutoff frequency in Hz
* `Q`: the quality factor
* `dtune`: detuning of the frequency in cents
#### Test
```faust
wa = library("webaudio.lib");
os = library("oscillators.lib");
highpass2_test = os.osc(440) : wa.highpass2(1000, 0.707, 0);
```
#### References
* <https://searchfox.org/mozilla-central/source/dom/media/webaudio/blink/Biquad.cpp#127>

---

## wa.bandpass2

--------------`(wa.)bandpass2`--------------
Standard second-order bandpass filter.
Frequencies outside the given range of frequencies are attenuated, the frequencies inside it pass through.
#### Usage
```faust
_ : bandpass2(f0, Q, dtune) : _
```
Where:
* `f0`: cutoff frequency in Hz
* `Q`: the quality factor
* `dtune`: detuning of the frequency in cents
#### Test
```faust
wa = library("webaudio.lib");
os = library("oscillators.lib");
bandpass2_test = os.osc(440) : wa.bandpass2(1000, 1, 0);
```
#### References
* <https://searchfox.org/mozilla-central/source/dom/media/webaudio/blink/Biquad.cpp#334>

---

## wa.notch2

--------------`(wa.)notch2`--------------
Standard notch filter, also called a band-stop or band-rejection filter.
It is the opposite of a bandpass filter: frequencies outside the give range of frequencies
pass through, frequencies inside it are attenuated.
#### Usage
```faust
_ : notch2(f0, Q, dtune) : _
```
Where:
* `f0`: cutoff frequency in Hz
* `Q`: the quality factor
* `dtune`: detuning of the frequency in cents
#### Test
```faust
wa = library("webaudio.lib");
os = library("oscillators.lib");
notch2_test = os.osc(440) : wa.notch2(1000, 1, 0);
```
#### References
* <https://searchfox.org/mozilla-central/source/dom/media/webaudio/blink/Biquad.cpp#301>

---

## wa.allpass2

--------------`(wa.)allpass2`--------------
Standard second-order allpass filter. It lets all frequencies through,
but changes the phase-relationship between the various frequencies.
#### Usage
```faust
_ : allpass2(f0, Q, dtune) : _
```
Where:
* `f0`: cutoff frequency in Hz
* `Q`: the quality factor
* `dtune`: detuning of the frequency in cents
#### Test
```faust
wa = library("webaudio.lib");
os = library("oscillators.lib");
allpass2_test = os.osc(440) : wa.allpass2(1000, 1, 0);
```
#### References
* <https://searchfox.org/mozilla-central/source/dom/media/webaudio/blink/Biquad.cpp#268>

---

## wa.peaking2

--------------`(wa.)peaking2`--------------
Frequencies inside the range get a boost or an attenuation, frequencies outside it are unchanged.
#### Usage
```faust
_ : peaking2(f0, gain, Q, dtune) : _
```
Where:
* `f0`: cutoff frequency in Hz
* `gain`: the gain in dB
* `Q`: the quality factor
* `dtune`: detuning of the frequency in cents
#### Test
```faust
wa = library("webaudio.lib");
os = library("oscillators.lib");
peaking2_test = os.osc(440) : wa.peaking2(1000, 3, 1, 0);
```
#### References
* <https://searchfox.org/mozilla-central/source/dom/media/webaudio/blink/Biquad.cpp#233>

---

## wa.lowshelf2

--------------`(wa.)lowshelf2`--------------
Standard second-order lowshelf filter.
Frequencies lower than the frequency get a boost, or an attenuation, frequencies over it are unchanged.
```faust
_ : lowshelf2(f0, gain, dtune) : _
```
Where:
* `f0`: cutoff frequency in Hz
* `gain`: the gain in dB
* `dtune`: detuning of the frequency in cents
#### Test
```faust
wa = library("webaudio.lib");
os = library("oscillators.lib");
lowshelf2_test = os.osc(440) : wa.lowshelf2(500, 6, 0);
```
#### References
* <https://searchfox.org/mozilla-central/source/dom/media/webaudio/blink/Biquad.cpp#169>

---

## wa.highshelf2

--------------`(wa.)highshelf2`--------------
Standard second-order highshelf filter.
Frequencies higher than the frequency get a boost or an attenuation, frequencies lower than it are unchanged.
```faust
_ : highshelf2(f0, gain, dtune) : _
```
Where:
* `f0`: cutoff frequency in Hz
* `gain`: the gain in dB
* `dtune`: detuning of the frequency in cents
#### Test
```faust
wa = library("webaudio.lib");
os = library("oscillators.lib");
highshelf2_test = os.osc(440) : wa.highshelf2(2000, -6, 0);
```
#### References
<https://searchfox.org/mozilla-central/source/dom/media/webaudio/blink/Biquad.cpp#201>

---
