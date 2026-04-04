$base = "http://localhost:8080"
$ok = 0; $err = 0

$tests = @(
    "POST /promotion/sync/campaigns/full",
    "POST /promotion/sync/stats/full",
    "POST /promotion/sync/calendar/full",
    "GET  /promotion/db/campaigns/",
    "GET  /promotion/db/stats/",
    "GET  /promotion/db/calendar/",
    "POST /communications/sync/feedbacks/full",
    "POST /communications/sync/questions/full",
    "POST /communications/sync/claims/full",
    "GET  /communications/db/feedbacks/",
    "GET  /communications/db/questions/",
    "GET  /communications/db/claims/",
    "POST /tariffs/sync/commissions/",
    "POST /tariffs/sync/box/",
    "POST /tariffs/sync/pallet/",
    "POST /tariffs/sync/supply/",
    "GET  /tariffs/db/commissions/",
    "GET  /tariffs/db/box/",
    "GET  /tariffs/db/pallet/",
    "GET  /tariffs/db/supply/",
    "POST /analytics/sync/funnel/full",
    "POST /analytics/sync/stocks/full",
    "GET  /analytics/db/funnel/",
    "GET  /analytics/db/stocks/",
    "POST /reports/sync/stocks/",
    "POST /reports/sync/orders/",
    "POST /reports/sync/sales/",
    "GET  /reports/db/stocks/",
    "GET  /reports/db/orders/",
    "GET  /reports/db/sales/",
    "POST /finances/sync/full/",
    "POST /finances/sync/incremental/",
    "GET  /finances/db/"
)

foreach ($line in $tests) {
    $parts = $line.Trim().Split(" ", 2)
    $method = $parts[0].Trim()
    $path = $parts[1].Trim()
    try {
        $resp = Invoke-WebRequest -Method $method -Uri "$base$path" -TimeoutSec 30 -ErrorAction Stop
        $j = $resp.Content | ConvertFrom-Json
        $extra = ""
        if ($null -ne $j.synced) { $extra = "synced=$($j.synced)" }
        elseif ($null -ne $j.task_id) { $extra = "queued" }
        elseif ($null -ne $j.total) { $extra = "total=$($j.total)" }
        else { $extra = "ok" }
        Write-Host "OK  $($resp.StatusCode) $method $path => $extra"
        $ok++
    } catch {
        $code = $_.Exception.Response.StatusCode.value__
        Write-Host "ERR $method $path => $code"
        $err++
    }
}

Write-Host ""
Write-Host "TOTAL: $ok OK, $err ERR"
