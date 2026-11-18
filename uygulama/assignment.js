(function (global) {
  "use strict";

  function distanceKm(a, b) {
    if (!a || !b) return Number.POSITIVE_INFINITY;
    var rad = function (v) { return v * Math.PI / 180; };
    var dLat = rad(Number(b.lat) - Number(a.lat));
    var dLng = rad(Number(b.lng) - Number(a.lng));
    var h = Math.sin(dLat / 2) ** 2 + Math.cos(rad(Number(a.lat))) * Math.cos(rad(Number(b.lat))) * Math.sin(dLng / 2) ** 2;
    return 6371 * 2 * Math.atan2(Math.sqrt(h), Math.sqrt(1 - h));
  }

  function rankedAvailable(spyler, customer, excludedIds) {
    var excluded = new Set((excludedIds || []).map(String));
    return (spyler || [])
      .filter(function (spy) { return spy.available !== false && !excluded.has(String(spy.id)); })
      .map(function (spy) { return Object.assign({}, spy, { distanceKm: distanceKm(spy, customer) }); })
      .sort(function (a, b) {
        if (a.distanceKm !== b.distanceKm) return a.distanceKm - b.distanceKm;
        return Number(a.sayac || 0) - Number(b.sayac || 0);
      });
  }

  function nearestAvailableSpy(spyler, customer, excludedIds) {
    return rankedAvailable(spyler, customer, excludedIds)[0] || null;
  }

  function reddet(context) {
    var rejected = (context.rejectedIds || []).concat(String(context.currentSpyId));
    return { rejectedIds: rejected, nextSpy: nearestAvailableSpy(context.spyler, context.customer, rejected), reason: "rejected" };
  }

  function sureDolunca(context) {
    var result = reddet(context);
    result.reason = "timeout";
    return result;
  }

  global.AssignmentEngine = { distanceKm: distanceKm, nearestAvailableSpy: nearestAvailableSpy, reddet: reddet, sureDolunca: sureDolunca };
})(window);
