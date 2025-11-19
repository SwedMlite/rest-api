Param(
    [string]$BaseUrl = "http://127.0.0.1:8080"
)

function Invoke-Step {
    Param(
        [string]$Title,
        [ScriptBlock]$Action
    )

    Write-Host ""
    Write-Host "==== $Title ====" -ForegroundColor Cyan
    try {
        $result = & $Action
        if ($null -eq $result) {
            Write-Host "(немає тіла відповіді)"
        }
        elseif ($result -is [string]) {
            Write-Host $result
        }
        else {
            $result | ConvertTo-Json -Depth 10
        }
        return $result
    }
    catch {
        Write-Host "ПОМИЛКА: $($_.Exception.Message)" -ForegroundColor Red
        if ($_.Exception.Response -and $_.Exception.Response.Content) {
            Write-Host $_.Exception.Response.Content
        }
        throw
    }
}

Write-Host "Використовую базову адресу: $BaseUrl" -ForegroundColor Yellow

Invoke-Step "GET /health" {
    Invoke-RestMethod -Method Get -Uri "$BaseUrl/health"
} | Out-Null

$userPayload = @{
    firstName = "Oleh"
    lastName = "Shevchenko"
    birthDate = "1998-04-12"
    email = "oleh.shevchenko@example.com"
    active = $true
    role = "user"
}
$createdUser = Invoke-Step "POST /users" {
    Invoke-RestMethod -Method Post -Uri "$BaseUrl/users" -Body ($userPayload | ConvertTo-Json -Depth 3) -ContentType "application/json"
}
$newUserId = $createdUser.id
Write-Host "Новий користувач має id=$newUserId" -ForegroundColor Green

Invoke-Step "GET /users?name=Іва&birthFrom=1990-01-01&role=admin" {
    Invoke-RestMethod -Method Get -Uri "$BaseUrl/users?name=Іва&birthFrom=1990-01-01&role=admin"
} | Out-Null

Invoke-Step "GET /users/1" {
    Invoke-RestMethod -Method Get -Uri "$BaseUrl/users/1"
} | Out-Null

$updateUserPayload = @{
    email = "oleh.updated@example.com"
    active = $false
}
Invoke-Step "PUT /users/$newUserId" {
    Invoke-RestMethod -Method Put -Uri "$BaseUrl/users/$newUserId" -Body ($updateUserPayload | ConvertTo-Json) -ContentType "application/json"
} | Out-Null

Invoke-Step "DELETE /users/$newUserId" {
    Invoke-RestMethod -Method Delete -Uri "$BaseUrl/users/$newUserId"
} | Out-Null

$postPayload = @{
    title = "Security checklist"
    body = "Нагадування про 2FA та резервні ключі."
    link = "https://example.com/security"
    userId = 1
}
$createdPost = Invoke-Step "POST /posts" {
    Invoke-RestMethod -Method Post -Uri "$BaseUrl/posts" -Body ($postPayload | ConvertTo-Json) -ContentType "application/json"
}
$newPostId = $createdPost.id
Write-Host "Нова публікація має id=$newPostId" -ForegroundColor Green

Invoke-Step "GET /posts?title=Security" {
    Invoke-RestMethod -Method Get -Uri "$BaseUrl/posts?title=Security"
} | Out-Null

$updatePostPayload = @{
    body = "Оновлений опис із новими правилами."
}
Invoke-Step "PUT /posts/$newPostId" {
    Invoke-RestMethod -Method Put -Uri "$BaseUrl/posts/$newPostId" -Body ($updatePostPayload | ConvertTo-Json) -ContentType "application/json"
} | Out-Null

Invoke-Step "DELETE /posts/$newPostId" {
    Invoke-RestMethod -Method Delete -Uri "$BaseUrl/posts/$newPostId"
} | Out-Null

$commentPayload = @{
    body = "Чекаю на наступні оновлення!"
    userId = 2
    postId = 1
}
$createdComment = Invoke-Step "POST /comments" {
    Invoke-RestMethod -Method Post -Uri "$BaseUrl/comments" -Body ($commentPayload | ConvertTo-Json) -ContentType "application/json"
}
$newCommentId = $createdComment.id
Write-Host "Новий коментар має id=$newCommentId" -ForegroundColor Green

Invoke-Step "GET /comments" {
    Invoke-RestMethod -Method Get -Uri "$BaseUrl/comments"
} | Out-Null

Invoke-Step "GET /posts/1/comments?userId=2" {
    Invoke-RestMethod -Method Get -Uri "$BaseUrl/posts/1/comments?userId=2"
} | Out-Null

$updateCommentPayload = @{
    body = "Редагований коментар після доопрацювань."
}
Invoke-Step "PUT /comments/$newCommentId" {
    Invoke-RestMethod -Method Put -Uri "$BaseUrl/comments/$newCommentId" -Body ($updateCommentPayload | ConvertTo-Json) -ContentType "application/json"
} | Out-Null

Invoke-Step "DELETE /comments/$newCommentId" {
    Invoke-RestMethod -Method Delete -Uri "$BaseUrl/comments/$newCommentId"
} | Out-Null

Write-Host ""
Write-Host "Готово! Усі запити з README були виконані послідовно." -ForegroundColor Yellow
