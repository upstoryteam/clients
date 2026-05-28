/**
 * Growth brief impact calculators. Init via initBriefImpactCalcs().
 * Markup: .vis-impact-calc[data-formula="app_store_ratings_90d"] with .vis-calc-input rows.
 */
(function () {
  const FORMULAS = {
    app_store_ratings_90d: {
      inputs: ['mau', 'prompt', 'convert'],
      compute: function (v) {
        var monthly = v.mau * (v.prompt / 100) * (v.convert / 100);
        return Math.round(monthly * 3);
      },
      multiplier: function (result, baseline) {
        return Math.max(1, Math.round((result + baseline) / Math.max(baseline, 1)));
      },
    },
    umove_first_payment_lift: {
      inputs: ['signups', 'baseline', 'lift'],
      compute: function (v) {
        return Math.round(v.signups * (v.lift / 100));
      },
    },
  };

  function formatValue(input, raw) {
    if (input.format === 'percent') return raw + '%';
    return Number(raw).toLocaleString();
  }

  function readValues(root) {
    var values = {};
    root.querySelectorAll('.vis-calc-input').forEach(function (row) {
      var id = row.getAttribute('data-id');
      var slider = row.querySelector('.vis-calc-slider');
      if (id && slider) values[id] = parseFloat(slider.value);
    });
    return values;
  }

  function updateCalc(root) {
    var formulaKey = root.getAttribute('data-formula');
    var spec = FORMULAS[formulaKey];
    if (!spec) return;

    var values = readValues(root);
    root.querySelectorAll('.vis-calc-input').forEach(function (row) {
      var id = row.getAttribute('data-id');
      var format = row.getAttribute('data-format');
      var slider = row.querySelector('.vis-calc-slider');
      var valEl = row.querySelector('.vis-calc-value');
      if (slider && valEl && id) {
        valEl.textContent = format === 'percent' ? slider.value + '%' : Number(slider.value).toLocaleString();
      }
    });

    var result = spec.compute(values);
    var outEl = root.querySelector('[data-calc-output]');
    if (outEl) outEl.textContent = result.toLocaleString();

    var multEl = root.querySelector('[data-calc-multiplier]');
    if (multEl && spec.multiplier) {
      var baseline = parseFloat(root.getAttribute('data-baseline') || '0');
      multEl.textContent = spec.multiplier(result, baseline) + '×';
    }
  }

  function bindCalc(root) {
    root.querySelectorAll('.vis-calc-slider').forEach(function (slider) {
      slider.addEventListener('input', function () {
        updateCalc(root);
      });
    });
    updateCalc(root);
  }

  function initBriefImpactCalcs() {
    document.querySelectorAll('.vis-impact-calc').forEach(bindCalc);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initBriefImpactCalcs);
  } else {
    initBriefImpactCalcs();
  }

  window.initBriefImpactCalcs = initBriefImpactCalcs;
})();
