import os
from flask import Flask, request

app = Flask(__name__)

# =========================================================
# [[ 1. THE SOSIX SCRIPT ]]
# =========================================================
MY_LUASCRIPT = r"""
--[[
              SOSIX HUB
          The Forge: World II
           Updated 12/29/2025
]]--

local TweenService = game:GetService("TweenService")
local UserInputService = game:GetService("UserInputService")
local RunService = game:GetService("RunService")
local VirtualInputManager = game:GetService("VirtualInputManager") -- Added for Clicker
local Player = game.Players.LocalPlayer

local ScreenGui = Instance.new("ScreenGui")
ScreenGui.Name = "SoSixHubGui"
ScreenGui.Parent = game.CoreGui
ScreenGui.ZIndexBehavior = Enum.ZIndexBehavior.Sibling

-- [[ SONIX ADDITION: CLICKER CIRCLE ]]
local ClickerCircle = Instance.new("Frame")
ClickerCircle.Name = "ClickerCircle"
ClickerCircle.Parent = ScreenGui
ClickerCircle.Size = UDim2.new(0, 50, 0, 50)
ClickerCircle.Position = UDim2.new(0.5, -25, 0.5, -25)
ClickerCircle.BackgroundColor3 = Color3.fromRGB(170, 0, 255)
ClickerCircle.BackgroundTransparency = 0.6
ClickerCircle.Visible = false
ClickerCircle.ZIndex = 999
Instance.new("UICorner", ClickerCircle).CornerRadius = UDim.new(1, 0)
local ClickStroke = Instance.new("UIStroke", ClickerCircle)
ClickStroke.Thickness = 2
ClickStroke.Color = Color3.fromRGB(255, 255, 255)

-- Draggable Logic (Circle)
local cDragging, cDragStart, cStartPos = false, nil, nil
ClickerCircle.InputBegan:Connect(function(i) 
    if i.UserInputType == Enum.UserInputType.MouseButton1 or i.UserInputType == Enum.UserInputType.Touch then 
        cDragging = true; cDragStart = i.Position; cStartPos = ClickerCircle.Position 
    end 
end)
UserInputService.InputChanged:Connect(function(i) 
    if cDragging and (i.UserInputType == Enum.UserInputType.MouseMovement or i.UserInputType == Enum.UserInputType.Touch) then 
        local delta = i.Position - cDragStart
        ClickerCircle.Position = UDim2.new(cStartPos.X.Scale, cStartPos.X.Offset + delta.X, cStartPos.Y.Scale, cStartPos.Y.Offset + delta.Y) 
    end 
end)
UserInputService.InputEnded:Connect(function() cDragging = false end)

local function TriggerTap()
    local x = ClickerCircle.AbsolutePosition.X + (ClickerCircle.AbsoluteSize.X / 2)
    local y = ClickerCircle.AbsolutePosition.Y + (ClickerCircle.AbsoluteSize.Y / 2)
    VirtualInputManager:SendMouseButtonEvent(x, y, 0, true, game, 0)
    task.wait(0.02)
    VirtualInputManager:SendMouseButtonEvent(x, y, 0, false, game, 0)
end

-- [[ MAIN CONTAINER (ORIGINAL) ]]
local MainFrame = Instance.new("Frame")
MainFrame.Name = "SoSixMain"
MainFrame.Parent = ScreenGui
MainFrame.BackgroundColor3 = Color3.fromRGB(255, 255, 255)
MainFrame.AnchorPoint = Vector2.new(0.5, 0.5)
MainFrame.Position = UDim2.new(0.5, 0, 0.5, 0)
MainFrame.Size = UDim2.new(0, 120, 0, 30)
MainFrame.Active = true
MainFrame.ClipsDescendants = true
Instance.new("UICorner", MainFrame).CornerRadius = UDim.new(0, 8)

local MainStroke = Instance.new("UIStroke", MainFrame)
MainStroke.Thickness = 2
MainStroke.Color = Color3.fromRGB(170, 0, 255)
MainStroke.ApplyStrokeMode = Enum.ApplyStrokeMode.Border

local UIGradient = Instance.new("UIGradient", MainFrame)
UIGradient.Color = ColorSequence.new{
    ColorSequenceKeypoint.new(0, Color3.fromRGB(20, 5, 35)),
    ColorSequenceKeypoint.new(0.5, Color3.fromRGB(80, 10, 150)),
    ColorSequenceKeypoint.new(1, Color3.fromRGB(20, 5, 35))    
}

RunService.RenderStepped:Connect(function(delta)
    UIGradient.Rotation = UIGradient.Rotation + (20 * delta)
    if UIGradient.Rotation >= 360 then UIGradient.Rotation = 0 end
end)

-- TOGGLE BUTTON
local ToggleBtn = Instance.new("TextButton", MainFrame)
ToggleBtn.Name = "Toggle"
ToggleBtn.Size = UDim2.new(1, 0, 0, 30)
ToggleBtn.BackgroundTransparency = 1
ToggleBtn.Text = "SOSIX"
ToggleBtn.TextColor3 = Color3.fromRGB(190, 80, 255)
ToggleBtn.Font = Enum.Font.GothamBold
ToggleBtn.TextSize = 12
ToggleBtn.ZIndex = 100

-- TITLE & SUBTITLE
local MainTitle = Instance.new("TextLabel", MainFrame)
MainTitle.Position = UDim2.new(0, 12, 0, 8)
MainTitle.Size = UDim2.new(0, 150, 0, 20)
MainTitle.BackgroundTransparency = 1
MainTitle.Text = "SOSIX HUB"
MainTitle.TextColor3 = Color3.fromRGB(190, 80, 255)
MainTitle.Font = Enum.Font.GothamBold
MainTitle.TextSize = 18
MainTitle.TextXAlignment = Enum.TextXAlignment.Left
MainTitle.Visible = false

local SubTitle = Instance.new("TextLabel", MainFrame)
SubTitle.Position = UDim2.new(0, 12, 0, 26)
SubTitle.Size = UDim2.new(0, 150, 0, 15)
SubTitle.BackgroundTransparency = 1
SubTitle.Text = "The Forge: World II"
SubTitle.TextColor3 = Color3.fromRGB(150, 150, 150)
SubTitle.Font = Enum.Font.GothamSemibold
SubTitle.TextSize = 10
SubTitle.TextXAlignment = Enum.TextXAlignment.Left
SubTitle.Visible = false

-- SIDEBAR
local Sidebar = Instance.new("Frame", MainFrame)
Sidebar.Name = "Sidebar"
Sidebar.Size = UDim2.new(0, 75, 1, -55)
Sidebar.Position = UDim2.new(0, 10, 0, 48)
Sidebar.BackgroundTransparency = 1
Sidebar.Visible = false
local SideLayout = Instance.new("UIListLayout", Sidebar)
SideLayout.Padding = UDim.new(0, 5)

-- SCROLLER
local ScrollContainer = Instance.new("ScrollingFrame", MainFrame)
ScrollContainer.Name = "ScrollContainer"
ScrollContainer.Size = UDim2.new(1, -100, 1, -55)
ScrollContainer.Position = UDim2.new(0, 90, 0, 48)
ScrollContainer.BackgroundTransparency = 1
ScrollContainer.ScrollBarThickness = 2
ScrollContainer.ScrollBarImageColor3 = Color3.fromRGB(170, 0, 255)
ScrollContainer.Visible = false
local ContentLayout = Instance.new("UIListLayout", ScrollContainer)
ContentLayout.Padding = UDim.new(0, 5)
ContentLayout.HorizontalAlignment = Enum.HorizontalAlignment.Center

-- [[ SONIX ADDITION: MINING VARIABLES ]]
local AutoMineActive = false
local SelectedRock = "Basalt Rock"
local RockList = {"Basalt Rock", "Basalt Core", "Basalt Vein", "Volcanic Rock"}
local RockIndex = 1

-- Independent Move Function for Miner (Does not interfere with TP system)
local function MinerMove(targetCFrame)
    local char = Player.Character
    if not char or not char:FindFirstChild("HumanoidRootPart") then return end
    local dist = (targetCFrame.Position - char.HumanoidRootPart.Position).Magnitude
    local speed = 40 -- Safe speed for mining
    local tween = TweenService:Create(char.HumanoidRootPart, TweenInfo.new(dist/speed, Enum.EasingStyle.Linear), {CFrame = targetCFrame})
    tween:Play()
    return tween
end

-- Mining Loop
task.spawn(function()
    while task.wait(0.2) do
        if AutoMineActive and Player.Character then
            local targetRock = nil
            local minDist = math.huge
            for _, v in pairs(workspace:GetDescendants()) do
                if v.Name == SelectedRock or (v:IsA("TextLabel") and v.Text:find(SelectedRock)) then
                    local model = v:FindFirstAncestorOfClass("Model") or v.Parent
                    local part = model:FindFirstChildWhichIsA("BasePart", true)
                    if part then
                        local d = (part.Position - Player.Character.HumanoidRootPart.Position).Magnitude
                        if d < minDist then minDist = d; targetRock = part end
                    end
                end
            end
            if targetRock then
                local tool = Player.Backpack:FindFirstChild("Pickaxe") or Player.Character:FindFirstChild("Pickaxe")
                if tool then
                    if tool.Parent ~= Player.Character then Player.Character.Humanoid:EquipTool(tool); task.wait(0.3) end
                    local rockPos = targetRock.CFrame * CFrame.new(0, 0, 3)
                    if (targetRock.Position - Player.Character.HumanoidRootPart.Position).Magnitude > 7 then
                        local t = MinerMove(rockPos); if t then t.Completed:Wait() end
                    end
                    tool:Activate()
                    TriggerTap()
                end
            end
        end
    end
end)

-- TP SYSTEM (ORIGINAL)
local LastPos = nil
local IsTeleporting = false
local AtNPC = false
local TravelSpeed = 85
local Buttons = {}

local function FindNPCByText(searchText)
    for _, v in pairs(workspace:GetDescendants()) do
        if v:IsA("Model") and v.Name:lower():find(searchText:lower()) then return v end
    end
    for _, v in pairs(workspace:GetDescendants()) do
        if v:IsA("TextLabel") and v.Text:lower():find(searchText:lower()) then
            return v:FindFirstAncestorOfClass("Model") or v.Parent
        end
    end
    return nil
end

-- UPDATED BUTTON FUNCTION (Supports Mode to protect TP logic)
local function AddMenuButton(txt, npcSearch, tabName, specialMode)
    local b = Instance.new("TextButton", ScrollContainer)
    b.Name = tabName
    b.Size = UDim2.new(0.9, 0, 0, 30)
    b.BackgroundColor3 = Color3.fromRGB(55, 20, 100)
    b.Text = txt
    b.TextColor3 = Color3.fromRGB(255, 255, 255)
    b.Font = Enum.Font.GothamBold
    b.TextSize = 11
    b.Visible = false
    Instance.new("UICorner", b).CornerRadius = UDim.new(0, 4)
    table.insert(Buttons, b)

    b.MouseButton1Click:Connect(function()
        -- [[ BRANCH 1: MINING & SELECTOR LOGIC ]]
        -- This ensures we DO NOT run TP logic for these buttons
        if specialMode == "Mine" then
            AutoMineActive = not AutoMineActive
            ClickerCircle.Visible = AutoMineActive
            b.Text = AutoMineActive and "Auto Mine: ON" or "Auto Mine: OFF"
            b.BackgroundColor3 = AutoMineActive and Color3.fromRGB(0, 180, 50) or Color3.fromRGB(55, 20, 100)
            return -- Exit, do not touch TP variables
        elseif specialMode == "Selector" then
            RockIndex = (RockIndex % #RockList) + 1
            SelectedRock = RockList[RockIndex]
            b.Text = "Target: " .. SelectedRock
            return -- Exit, do not touch TP variables
        end

        -- [[ BRANCH 2: ORIGINAL TP LOGIC ]]
        -- Only runs if not a special mode. Preserved exactly as requested.
        if IsTeleporting or (AtNPC and b.Text ~= "TP Back" and b.Name == "Teleport") then return end
        
        local char = Player.Character
        local targetNPC = (npcSearch ~= "") and FindNPCByText(npcSearch) or nil
        if not char or (npcSearch ~= "" and not targetNPC) then return end
        
        IsTeleporting = true
        
        if b.Name == "Teleport" then
            for _, other in pairs(Buttons) do 
                if other.Name == "Teleport" then
                    if other ~= b then other.BackgroundColor3 = Color3.fromRGB(100, 0, 0) else b.BackgroundColor3 = Color3.fromRGB(0, 180, 50) end
                end
            end
        end

        local startCF = char.HumanoidRootPart.CFrame
        local endCF
        
        if b.Text == "TP Back" then
            endCF = LastPos
        elseif targetNPC then
            LastPos = startCF
            local targetPart = targetNPC:FindFirstChild("HumanoidRootPart") or targetNPC:FindFirstChild("Head") or targetNPC:FindFirstChildWhichIsA("BasePart")
            local groundPos = targetPart.CFrame * CFrame.new(0, -3.2, -5) 
            endCF = CFrame.new(groundPos.Position, Vector3.new(targetPart.Position.X, groundPos.Position.Y, targetPart.Position.Z))
        end

        if endCF then
            local dist = (endCF.Position - char.HumanoidRootPart.Position).Magnitude
            local tween = TweenService:Create(char.HumanoidRootPart, TweenInfo.new(dist/TravelSpeed, Enum.EasingStyle.Linear), {CFrame = endCF})
            tween:Play()
            tween.Completed:Wait()

            if b.Text == "TP Back" then
                b.Text = txt; AtNPC = false
                for _, other in pairs(Buttons) do if other.Name == "Teleport" then other.BackgroundColor3 = Color3.fromRGB(55, 20, 100) end end
            else
                b.Text = "TP Back"; AtNPC = true
            end
        end
        IsTeleporting = false
    end)
end

-- TABS
local function CreateTab(name)
    local btn = Instance.new("TextButton", Sidebar)
    btn.Size = UDim2.new(1, 0, 0, 28)
    btn.BackgroundColor3 = Color3.fromRGB(45, 15, 85)
    btn.Text = name
    btn.TextColor3 = Color3.fromRGB(255, 255, 255)
    btn.Font = Enum.Font.GothamBold
    btn.TextSize = 10
    Instance.new("UICorner", btn).CornerRadius = UDim.new(0, 4)
    return btn
end

local AutoTab = CreateTab("Auto")
local TPTab = CreateTab("Teleport")
local InfoTab = CreateTab("Info")

-- BUTTONS SETUP (TELEPORT)
AddMenuButton("Potion Shop", "Maria", "Teleport")
AddMenuButton("Pickaxe Shop", "Miner Fred", "Teleport")
AddMenuButton("Sell Items", "Greedy Cey", "Teleport")
AddMenuButton("Fisher", "Fisher", "Teleport")
AddMenuButton("Forge", "Sensei Moro", "Teleport")
AddMenuButton("Wizard", "Wizard", "Teleport")
AddMenuButton("Enhancer", "Enhancer", "Teleport")
AddMenuButton("Runemaker", "Runemaker", "Teleport")

-- AUTO TAB (UPDATED)
AddMenuButton("Target: Basalt Rock", "", "Auto", "Selector") -- New Selector
AddMenuButton("Auto Mine: OFF", "", "Auto", "Mine")          -- New Auto Mine

-- INFO TAB
AddMenuButton("Script: Sonix Hub", "", "Info")
AddMenuButton("Version: 2.3", "", "Info")
AddMenuButton("Status: Active", "", "Info")

-- TAB SWITCHING
local function ShowTab(name)
    for _, item in pairs(ScrollContainer:GetChildren()) do
        if item:IsA("TextButton") then item.Visible = (item.Name == name) end
    end
end

AutoTab.MouseButton1Click:Connect(function() ShowTab("Auto") end)
TPTab.MouseButton1Click:Connect(function() ShowTab("Teleport") end)
InfoTab.MouseButton1Click:Connect(function() ShowTab("Info") end)

-- DRAGGING
local dragging, dragStart, startPos, hasMoved = false, nil, nil, false
ToggleBtn.InputBegan:Connect(function(i) 
    if i.UserInputType == Enum.UserInputType.MouseButton1 or i.UserInputType == Enum.UserInputType.Touch then 
        dragging, hasMoved = true, false 
        dragStart = i.Position; startPos = MainFrame.Position 
    end 
end)
UserInputService.InputChanged:Connect(function(i) 
    if dragging and (i.UserInputType == Enum.UserInputType.MouseMovement or i.UserInputType == Enum.UserInputType.Touch) then 
        local delta = i.Position - dragStart
        if delta.Magnitude > 2 then hasMoved = true end
        MainFrame.Position = UDim2.new(startPos.X.Scale, startPos.X.Offset + delta.X, startPos.Y.Scale, startPos.Y.Offset + delta.Y)
    end 
end)
UserInputService.InputEnded:Connect(function() dragging = false end)

-- TOGGLE OPEN/CLOSE
local opened, animating = false, false
ToggleBtn.MouseButton1Click:Connect(function()
    if hasMoved or animating then return end
    animating = true; opened = not opened
    if opened then
        ToggleBtn.Text = ""
        MainFrame:TweenSize(UDim2.new(0, 310, 0, 200), "Out", "Quart", 0.4, true)
        task.wait(0.2); MainTitle.Visible = true; SubTitle.Visible = true; Sidebar.Visible = true; ScrollContainer.Visible = true
        ShowTab("Teleport") 
    else
        MainTitle.Visible = false; SubTitle.Visible = false; Sidebar.Visible = false; ScrollContainer.Visible = false
        MainFrame:TweenSize(UDim2.new(0, 120, 0, 30), "In", "Quart", 0.4, true)
        task.wait(0.3); ToggleBtn.Text = "SOSIX"
    end
    animating = false
end)"""

@app.route('/')
def home():
    return "<h1>Access Denied</h1><p>Sonix Security Layer Active.</p>", 403

@app.route('/Blocker', methods=['GET'])
def load():
    # Get the User-Agent (identifies who is visiting the link)
    user_agent = request.headers.get('User-Agent', '').lower()
    
    # List of common web browsers to block
    browsers = ['mozilla', 'chrome', 'safari', 'edge', 'opera']
    
    # If a browser is visiting, show a fake "Blocked" or "Empty" page
    if any(browser in user_agent for browser in browsers):
        return "ERROR: Unauthorized Source Code Access. IP Logged.", 403

    # If it's NOT a browser (meaning it's likely an executor), send the script
    return MY_LUASCRIPT, 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
