# CuratorAI MVP - Continuation Wireframes & Design System

## 📐 Complete Design System

### Spacing Scale
```
2px   ▏ Micro spacing
4px   ▎ Tight spacing
8px   ▍ Small spacing
12px  ▌ Compact spacing
16px  ▋ Base unit (1rem)
24px  ▊ Medium spacing
32px  ▉ Large spacing
48px  █ XL spacing
64px  ██ XXL spacing
96px  ███ Hero spacing
```

### Grid System
```
┌─────────────────────────────────────────────────────────────┐
│ [Container: 1440px max-width]                               │
│ ┌─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┐ 12 Column Grid                  │
│ │ │ │ │ │ │ │ │ │ │ │ │ │ Gutter: 24px                    │
│ └─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┘                                  │
│                                                             │
│ Breakpoints:                                                │
│ Mobile:  320px - 767px   (4 columns, 16px gutter)          │
│ Tablet:  768px - 1023px  (8 columns, 20px gutter)          │
│ Desktop: 1024px+          (12 columns, 24px gutter)        │
└─────────────────────────────────────────────────────────────┘
```

### Typography Scale
```
H1: 48px/56px - Bold - #111827 - Hero Headlines
H2: 36px/44px - Bold - #111827 - Page Titles
H3: 30px/36px - SemiBold - #111827 - Section Headers
H4: 24px/32px - SemiBold - #111827 - Card Titles
H5: 20px/28px - Medium - #111827 - Subsections
H6: 18px/24px - Medium - #374151 - Small Headers

Body Large:  18px/28px - Regular - #374151
Body:        16px/24px - Regular - #374151
Body Small:  14px/20px - Regular - #6B7280
Caption:     12px/16px - Regular - #9CA3AF
Overline:    12px/16px - Bold - #6B7280 - Uppercase
```

### Elevation System
```
Level 0: None           - Base surface
Level 1: 0 1px 2px      - Subtle lift (cards)
Level 2: 0 4px 8px      - Raised (hover states)
Level 3: 0 8px 16px     - Floating (modals)
Level 4: 0 16px 32px    - Overlay (dropdowns)
Level 5: 0 24px 48px    - Maximum (important dialogs)

Shadow Colors: rgba(0, 0, 0, 0.1) - Light
               rgba(0, 0, 0, 0.15) - Medium
               rgba(0, 0, 0, 0.2) - Strong
```

### Component States
```
┌──────────────────────────────────────────────────────────┐
│ State      │ Background │ Border    │ Text     │ Icon   │
├──────────────────────────────────────────────────────────┤
│ Default    │ #FFFFFF    │ #E5E7EB   │ #111827  │ #6B7280│
│ Hover      │ #F9FAFB    │ #6366F1   │ #111827  │ #6366F1│
│ Active     │ #EEF2FF    │ #6366F1   │ #4F46E5  │ #4F46E5│
│ Focus      │ #FFFFFF    │ #6366F1   │ #111827  │ #6366F1│
│            │            │ +Ring 4px │          │        │
│ Disabled   │ #F3F4F6    │ #E5E7EB   │ #D1D5DB  │ #D1D5DB│
│ Error      │ #FEF2F2    │ #EF4444   │ #991B1B  │ #EF4444│
│ Success    │ #F0FDF4    │ #10B981   │ #065F46  │ #10B981│
└──────────────────────────────────────────────────────────┘
```

### Animation Timing
```
Micro:      100ms - Icons, small elements
Fast:       200ms - Buttons, hovers
Base:       300ms - Default transitions
Moderate:   400ms - Modals, panels
Slow:       600ms - Page transitions
Gentle:     800ms - Relaxed animations

Easing:
- ease-in-out: Default for most
- ease-out: Entrances
- ease-in: Exits
- spring: Playful interactions
```

---

## 🔐 Authentication Enhancements

### Password Reset Flow

```
╔══════════════════════════════════════════════════════════════╗
║  [← Back]            Reset Password                          ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║                    🔒 Forgot Password?                       ║
║                                                              ║
║     No worries! Enter your email and we'll send you          ║
║              a link to reset your password                   ║
║                                                              ║
║  ┌──────────────────────────────────────────────────────┐   ║
║  │ Email Address                                        │   ║
║  │ [________________]  [✓]                              │   ║
║  │ (Border: #E5E7EB, Focus: #6366F1 + Ring)            │   ║
║  └──────────────────────────────────────────────────────┘   ║
║                                                              ║
║  ┌──────────────────────────────────────────────────────┐   ║
║  │         [Send Reset Link →]                          │   ║
║  │      (Primary #6366F1, Full Width)                   │   ║
║  │   [Hover: Scale 1.02, Shadow Level 2]                │   ║
║  └──────────────────────────────────────────────────────┘   ║
║                                                              ║
║              Remember your password? [Login]                 ║
║                  (Link - #6366F1)                           ║
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │ 💡 Tips:                                               │ ║
║  │ • Check your spam folder                               │ ║
║  │ • Link expires in 1 hour                               │ ║
║  │ • Contact support if you don't receive it              │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Success State - Email Sent

```
╔══════════════════════════════════════════════════════════════╗
║  [← Back]         Check Your Email                          ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║                         ✉️                                   ║
║                  (Animated bounce)                           ║
║                                                              ║
║                   Email Sent! 🎉                             ║
║                                                              ║
║     We've sent a password reset link to:                     ║
║              sarah@email.com                                 ║
║                                                              ║
║     Click the link in your email to reset your password      ║
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │              [Open Email App]                          │ ║
║  │           (Primary #6366F1)                            │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║     Didn't receive the email?                                ║
║     [Resend] (Available in 00:45)                            ║
║     (Countdown timer animation)                              ║
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │ 🔐 Security Note:                                      │ ║
║  │ For your security, this link will expire in 1 hour     │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### New Password Creation

```
╔══════════════════════════════════════════════════════════════╗
║  [← Back]         Create New Password                       ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║                  Choose a Strong Password                    ║
║                                                              ║
║  ┌──────────────────────────────────────────────────────┐   ║
║  │ New Password                                         │   ║
║  │ [••••••••••••••]  [👁]                              │   ║
║  │                                                      │   ║
║  │ Password Strength:                                   │   ║
║  │ [████████░░░░░░░░] Strong                           │   ║
║  │ (Color: Weak #EF4444, Medium #F59E0B, Strong #10B981)│  ║
║  └──────────────────────────────────────────────────────┘   ║
║                                                              ║
║  Requirements:                                               ║
║  ✅ At least 8 characters    (#10B981)                       ║
║  ✅ One uppercase letter                                     ║
║  ✅ One lowercase letter                                     ║
║  ✅ One number                                               ║
║  ⭕ One special character    (#E5E7EB - pending)             ║
║  (Animated checkmarks on completion)                         ║
║                                                              ║
║  ┌──────────────────────────────────────────────────────┐   ║
║  │ Confirm Password                                     │   ║
║  │ [••••••••••••••]  [👁]                              │   ║
║  │ ✓ Passwords match                                    │   ║
║  └──────────────────────────────────────────────────────┘   ║
║                                                              ║
║  ┌──────────────────────────────────────────────────────┐   ║
║  │         [Reset Password →]                           │   ║
║  │      (Primary #6366F1, Disabled until valid)         │   ║
║  └──────────────────────────────────────────────────────┘   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Email Verification

```
╔══════════════════════════════════════════════════════════════╗
║             Verify Your Email Address                        ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║                         📧                                   ║
║                  (Pulse animation)                           ║
║                                                              ║
║              One More Step, Sarah! 👋                        ║
║                                                              ║
║  We've sent a verification code to:                          ║
║              sarah@email.com                                 ║
║                                                              ║
║  Enter the 6-digit code:                                     ║
║                                                              ║
║  ┌─────┐ ┌─────┐ ┌─────┐   ┌─────┐ ┌─────┐ ┌─────┐        ║
║  │  5  │ │  4  │ │  7  │   │  _  │ │  _  │ │  _  │        ║
║  └─────┘ └─────┘ └─────┘   └─────┘ └─────┘ └─────┘        ║
║  (Large inputs, auto-focus next, #6366F1 border on focus)   ║
║                                                              ║
║  ⏱️ Code expires in: 09:45                                   ║
║  (Countdown timer - turns #EF4444 under 1 minute)           ║
║                                                              ║
║  ┌──────────────────────────────────────────────────────┐   ║
║  │              [Verify Email]                          │   ║
║  │     (Auto-submit when 6 digits entered)              │   ║
║  └──────────────────────────────────────────────────────┘   ║
║                                                              ║
║     Didn't receive the code?                                 ║
║     [Resend Code] [Change Email]                             ║
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │ 💡 Tip: Check your spam or junk folder                │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 🎯 Virtual Try-On Interface

### Camera Setup & Permissions

```
╔══════════════════════════════════════════════════════════════╗
║  [✕]            Virtual Try-On              [Skip Tutorial] ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║                    Welcome to Try-On! 🎨                     ║
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │                                                        │ ║
║  │              [3D Avatar Preview]                       │ ║
║  │           (Rotating animation)                         │ ║
║  │                                                        │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║              See outfits on yourself in real-time!           ║
║                                                              ║
║  What you'll need:                                           ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │ 📷 Camera Access                                       │ ║
║  │    We need to see you to overlay clothes               │ ║
║  │                                                        │ ║
║  │ 🧍 Full Body View                                      │ ║
║  │    Stand 3-4 feet from camera                          │ ║
║  │                                                        │ ║
║  │ 💡 Good Lighting                                       │ ║
║  │    Natural or bright indoor light works best           │ ║
║  │                                                        │ ║
║  │ 📐 Space to Move                                       │ ║
║  │    Turn around to see all angles                       │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  ┌──────────────────────────────────────────────────────┐   ║
║  │         [Enable Camera & Start →]                    │   ║
║  │           (Primary #6366F1)                          │   ║
║  └──────────────────────────────────────────────────────┘   ║
║                                                              ║
║                [View Sample Try-On Demo ▶]                   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Live Try-On Interface

```
╔══════════════════════════════════════════════════════════════╗
║ [✕]  Virtual Try-On                        [Settings ⚙️]    ║
╠══════════════════════════════════════════════════════════════╣
║ ┌────────────────────────────────────────────────────────┐  ║
║ │                                                        │  ║
║ │              [Live Camera Feed]                        │  ║
║ │         (Real-time AR overlay)                         │  ║
║ │                                                        │  ║
║ │  ┌──────────────────┐                                 │  ║
║ │  │ Body Tracking:   │  🟢 Excellent                   │  ║
║ │  │ Lighting:        │  🟡 Good                        │  ║
║ │  │ Distance:        │  🟢 Perfect                     │  ║
║ │  └──────────────────┘                                 │  ║
║ │                                                        │  ║
║ │         [User with virtual clothing overlay]           │  ║
║ │                                                        │  ║
║ │  [🔄]  [📸]  [❤️]  [🛒]                               │  ║
║ │  Rotate Capture Like  Buy                             │  ║
║ │                                                        │  ║
║ └────────────────────────────────────────────────────────┘  ║
║                                                              ║
║  Current Item: Blue Summer Dress                             ║
║  [< Previous]  [Next >]                                      ║
║                                                              ║
║  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐             ║
║  │[Img] │ │[Img] │ │[Img] │ │[Img] │ │[Img] │             ║
║  │ 👗   │ │ 👕   │ │ 👖   │ │ 👔   │ │ 👟   │             ║
║  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘             ║
║  (Horizontal scroll, active item highlighted)                ║
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │ 💡 Tips:                                               │ ║
║  │ • Turn around slowly to see all angles                 │ ║
║  │ • Tap garment to adjust fit                            │ ║
║  │ • Pinch to zoom in/out                                 │ ║
║  │ [Tutorial ▶]                                           │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  [Share 📤] [Save to Wardrobe 💾] [Different Lighting 💡]   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Try-On Calibration

```
╔══════════════════════════════════════════════════════════════╗
║           Body Measurement Setup                             ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Let's get your measurements for accurate fit! 📏            ║
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │              [Silhouette Outline]                      │ ║
║  │                                                        │ ║
║  │               ┌───┐    ← Head                         │ ║
║  │               │ ○ │                                    │ ║
║  │               └───┘                                    │ ║
║  │            ╱─┬───┬─╲  ← Shoulders                     │ ║
║  │           ╱  │   │  ╲                                 │ ║
║  │          ┃   │   │   ┃ ← Chest                        │ ║
║  │          ┃   │   │   ┃                                │ ║
║  │          ┃───┼───┼───┃ ← Waist                        │ ║
║  │          ┃   │   │   ┃                                │ ║
║  │         ╱┃   │   │   ┃╲ ← Hips                        │ ║
║  │        ╱ │   │   │   │ ╲                              │ ║
║  │       │  │   │   │   │  │                             │ ║
║  │       │  │   │   │   │  │ ← Inseam                    │ ║
║  │       └──┘   └───┘   └──┘                             │ ║
║  │                                                        │ ║
║  │  Stand 3-4 feet away, arms slightly away from body    │ ║
║  │                                                        │ ║
║  │  [Auto-Detect Active]  Progress: ███████░░  75%       │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  Detected Measurements:                                      ║
║  • Height: 5'6" (168 cm)                                     ║
║  • Shoulders: 16" (41 cm)                                    ║
║  • Chest: 34" (86 cm)                                        ║
║  • Waist: 28" (71 cm)                                        ║
║  • Hips: 38" (97 cm)                                         ║
║                                                              ║
║  [✏️ Edit Manually] [Retake] [Looks Good! Continue →]       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 📱 Enhanced Mobile Interactions

### Swipe Gestures

```
╔══════════════════════════════════════════════════════════════╗
║                  Swipeable Post Card                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Default State:                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │ [@username] · 2h ago                                   │ ║
║  │ [Post Image]                                           │ ║
║  │ Summer vibes 🌞 #OOTD                                  │ ║
║  │ ❤️ 234  💬 12                                          │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  Swipe Left → (Reveal Actions)                              ║
║  ┌────────────────────────────────┬──────┬──────┬──────┐   ║
║  │ [@username] · 2h ago           │  🔖  │  ↗   │  •••  │   ║
║  │ [Post Image]                   │ Save │ Share│ More │   ║
║  │ Summer vibes 🌞                │      │      │      │   ║
║  └────────────────────────────────┴──────┴──────┴──────┘   ║
║  (Actions slide in from right, #6366F1 background)          ║
║                                                              ║
║  Swipe Right → (Quick Like)                                 ║
║  ┌──────┬────────────────────────────────────────────────┐ ║
║  │  ❤️  │ [@username] · 2h ago                          │ ║
║  │ +234 │ [Post Image]                                   │ ║
║  │      │ Summer vibes 🌞                                │ ║
║  └──────┴────────────────────────────────────────────────┘ ║
║  (Heart icon grows + bounce animation)                       ║
║                                                              ║
║  Pull Down → (Refresh)                                       ║
║         ↓                                                    ║
║       ⟳ 🔄                                                   ║
║  (Refresh indicator)                                         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Long Press Menus

```
╔══════════════════════════════════════════════════════════════╗
║              Long Press Context Menu                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  [User long-presses on wardrobe item]                        ║
║                                                              ║
║  ┌──────┐                                                    ║
║  │[Img] │ ← Item being pressed                               ║
║  │ 👕   │   (Slight scale up, shadow increase)              ║
║  └──────┘                                                    ║
║     ↓                                                        ║
║  ┌─────────────────────────────┐                            ║
║  │ 📝 Edit Item                │ (Haptic feedback)          ║
║  ├─────────────────────────────┤                            ║
║  │ 🔄 Add to Outfit            │                            ║
║  ├─────────────────────────────┤                            ║
║  │ ↗️  Share                    │                            ║
║  ├─────────────────────────────┤                            ║
║  │ 📊 View Stats               │                            ║
║  ├─────────────────────────────┤                            ║
║  │ 🗑️  Delete                   │ (#EF4444)                 ║
║  └─────────────────────────────┘                            ║
║  (Menu fades in 200ms, blur background)                      ║
║  (Tap outside to dismiss)                                    ║
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │ 💡 Interaction:                                        │ ║
║  │ • Haptic feedback on press start                       │ ║
║  │ • Menu appears after 500ms hold                        │ ║
║  │ • Release over option to select                        │ ║
║  │ • Slide to option while holding (iOS style)            │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Pull to Refresh Pattern

```
╔══════════════════════════════════════════════════════════════╗
║               Pull to Refresh States                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  State 1: Ready (Pull starts)                                ║
║       ↓ Pull down                                            ║
║       ○                                                      ║
║  ──────────────────────                                      ║
║  [Content below]                                             ║
║                                                              ║
║  State 2: Pulling (0-60px)                                   ║
║       ↓↓                                                     ║
║      ◐ (Rotating)                                            ║
║  ──────────────────────                                      ║
║  [Content moves down]                                        ║
║                                                              ║
║  State 3: Ready to Release (60px+)                           ║
║       ↓↓↓                                                    ║
║      ◉ Ready!                                                ║
║  ──────────────────────                                      ║
║  [Release to refresh]                                        ║
║  (Haptic feedback pulse)                                     ║
║                                                              ║
║  State 4: Refreshing                                         ║
║       ⟳                                                      ║
║      🔄 (Spinning)                                           ║
║  ──────────────────────                                      ║
║  [Content refreshing...]                                     ║
║  (Show new items count)                                      ║
║                                                              ║
║  State 5: Complete                                           ║
║       ✓                                                      ║
║      ✅ Updated!                                             ║
║  ──────────────────────                                      ║
║  [New content appears]                                       ║
║  (Brief success animation)                                   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Bottom Sheet Modal

```
╔══════════════════════════════════════════════════════════════╗
║             Mobile Bottom Sheet Pattern                      ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Background dimmed (rgba(0,0,0,0.4))                         ║
║  [Main content behind - blurred]                             ║
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │                    ───                                 │ ║
║  │              (Drag handle - #D1D5DB)                   │ ║
║  │                                                        │ ║
║  │  Filter Options                          [✕ Close]    │ ║
║  │  ═══════════════════════════════════════              │ ║
║  │                                                        │ ║
║  │  Price Range                                           │ ║
║  │  ○━━━━━━━━━━━━━━━━━━○                                │ ║
║  │  $50                $500                               │ ║
║  │                                                        │ ║
║  │  Category                                              │ ║
║  │  [All] [Tops] [Bottoms] [Shoes]                       │ ║
║  │                                                        │ ║
║  │  Size                                                  │ ║
║  │  [S] [M] [L] [XL]                                     │ ║
║  │                                                        │ ║
║  │  ┌───────────────┐  ┌────────────────┐               │ ║
║  │  │ Clear Filters │  │ Apply (24)     │               │ ║
║  │  └───────────────┘  └────────────────┘               │ ║
║  │                                                        │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  Interactions:                                               ║
║  • Swipe down to dismiss                                     ║
║  • Tap outside to close                                      ║
║  • Drag handle to resize (half/full)                         ║
║  • Springs back if not fully dragged                         ║
║  • Haptic feedback on open/close                             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Double Tap to Like

```
╔══════════════════════════════════════════════════════════════╗
║             Double Tap Interaction                           ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │                                                        │ ║
║  │              [Post Image]                              │ ║
║  │                                                        │ ║
║  │           Double tap anywhere →                        │ ║
║  │                                                        │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║                         ↓↓                                   ║
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │                                                        │ ║
║  │              [Post Image]                              │ ║
║  │                                                        │ ║
║  │                   ❤️                                   │ ║
║  │             (Scale: 0→2→1)                             │ ║
║  │          (Opacity: 0→1→0.8)                            │ ║
║  │            (Duration: 800ms)                           │ ║
║  │                                                        │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  Animation Sequence:                                         ║
║  1. Tap detected (0ms)                                       ║
║  2. Heart appears at tap point (50ms)                        ║
║  3. Scale up 0→2 (50-250ms) ease-out                        ║
║  4. Slight rotation ±5° (100-300ms)                         ║
║  5. Scale down 2→1 (250-500ms) ease-in                      ║
║  6. Fade out (500-800ms)                                     ║
║  7. Like count updates (haptic pulse)                        ║
║                                                              ║
║  State Changes:                                              ║
║  ❤️ 234 → ❤️ 235 (Color: #EF4444)                           ║
║  (Number animates up, brief scale pulse)                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

## ⚠️ Error States & Edge Cases

### Network Error

```
╔══════════════════════════════════════════════════════════════╗
║                 Connection Error                             ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║                                                              ║
║                    🌐 ⚠️                                     ║
║                 (Animated icon)                              ║
║                                                              ║
║                 No Internet Connection                       ║
║                                                              ║
║         Oops! It looks like you're offline.                  ║
║         Check your connection and try again.                 ║
║                                                              ║
║  ┌──────────────────────────────────────────────────────┐   ║
║  │              [Retry Connection]                      │   ║
║  │            (Primary #6366F1)                         │   ║
║  └──────────────────────────────────────────────────────┘   ║
║                                                              ║
║            [Go Offline Mode] [Settings]                      ║
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │ 💡 Offline Features Available:                        │ ║
║  │ • Browse saved outfits                                 │ ║
║  │ • View wardrobe                                        │ ║
║  │ • Explore lookbooks                                    │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  Auto-retry in: 5s ⟳                                         ║
║  (Countdown with auto-refresh)                               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Server Error (500)

```
╔══════════════════════════════════════════════════════════════╗
║                  Something Went Wrong                        ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║                                                              ║
║                    🔧 500                                     ║
║                (Sad robot icon)                              ║
║                                                              ║
║              Oops! Something went wrong                      ║
║                                                              ║
║      We're having trouble on our end. Our team has           ║
║      been notified and is working to fix this.               ║
║                                                              ║
║  ┌──────────────────────────────────────────────────────┐   ║
║  │              [Try Again]                             │   ║
║  │            (Primary #6366F1)                         │   ║
║  └──────────────────────────────────────────────────────┘   ║
║                                                              ║
║            [Go Back Home] [Contact Support]                  ║
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │ Error Code: 500-2025-10-16-1234                       │ ║
║  │ (For support reference)                                │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  Status: Checking server... 🔄                               ║
║  [View Status Page ↗]                                        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Permission Denied

```
╔══════════════════════════════════════════════════════════════╗
║                Camera Access Required                        ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║                                                              ║
║                    📷 🚫                                     ║
║                                                              ║
║              Camera Access Blocked                           ║
║                                                              ║
║    CuratorAI needs camera access to use virtual try-on       ║
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │ How to enable camera:                                  │ ║
║  │                                                        │ ║
║  │ iOS:                                                   │ ║
║  │ Settings → CuratorAI → Camera → Enable                │ ║
║  │                                                        │ ║
║  │ Android:                                               │ ║
║  │ Settings → Apps → CuratorAI → Permissions → Camera    │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  ┌──────────────────────────────────────────────────────┐   ║
║  │         [Open Settings]                              │   ║
║  │      (Opens device settings)                         │   ║
║  └──────────────────────────────────────────────────────┘   ║
║                                                              ║
║              [Not Now] [Learn More About Privacy]            ║
║                                                              ║
║  🔒 Your privacy matters                                     ║
║  Camera access is only used for try-on features.             ║
║  We never save or share your photos.                         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Upload Failed

```
╔══════════════════════════════════════════════════════════════╗
║                  Upload Failed                               ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │                                                        │ ║
║  │          [Preview of failed image]                     │ ║
║  │              (Dimmed, 50% opacity)                     │ ║
║  │                                                        │ ║
║  │                    ⚠️ ❌                               │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║              Upload Failed: File Too Large                   ║
║                                                              ║
║  Your image (15.2 MB) exceeds the 10 MB limit.               ║
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │ 💡 Solutions:                                          │ ║
║  │ • Use our compression tool below                       │ ║
║  │ • Choose a smaller image                               │ ║
║  │ • Take a new photo                                     │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  ┌──────────────────────────────────────────────────────┐   ║
║  │       [Compress & Retry]                             │   ║
║  │   (Will reduce to ~5MB automatically)                │   ║
║  └──────────────────────────────────────────────────────┘   ║
║                                                              ║
║        [Choose Different Image] [Cancel]                     ║
║                                                              ║
║  Other possible issues:                                      ║
║  [File format not supported] [Poor image quality]            ║
║  [Network timeout]                                           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Form Validation Errors

```
╔══════════════════════════════════════════════════════════════╗
║           Form with Validation Errors                        ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │ ⚠️ Please fix 3 errors before continuing              │ ║
║  │ (Error summary banner - #FEF2F2 bg, #EF4444 border)   │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  ┌──────────────────────────────────────────────────────┐   ║
║  │ Email Address                                    ✓   │   ║
║  │ [sarah@email.com____]                                │   ║
║  │ (Border: #10B981 - Valid)                            │   ║
║  └──────────────────────────────────────────────────────┘   ║
║                                                              ║
║  ┌──────────────────────────────────────────────────────┐   ║
║  │ Password                                         ❌  │   ║
║  │ [123_________________]                               │   ║
║  │ ⚠️ Password must be at least 8 characters            │   ║
║  │ (Border: #EF4444 - Error, shake animation)           │   ║
║  └──────────────────────────────────────────────────────┘   ║
║                                                              ║
║  ┌──────────────────────────────────────────────────────┐   ║
║  │ Confirm Password                                 ❌  │   ║
║  │ [abc_________________]                               │   ║
║  │ ⚠️ Passwords don't match                             │   ║
║  │ (Border: #EF4444 - Error)                            │   ║
║  └──────────────────────────────────────────────────────┘   ║
║                                                              ║
║  ┌──────────────────────────────────────────────────────┐   ║
║  │ Phone Number (Optional)                              │   ║
║  │ [_________________]                                  │   ║
║  │ (Border: #E5E7EB - Default, not required)            │   ║
║  └──────────────────────────────────────────────────────┘   ║
║                                                              ║
║  ┌──────────────────────────────────────────────────────┐   ║
║  │              [Continue]                              │   ║
║  │         (Disabled - #D1D5DB)                         │   ║
║  │     (Enabled when all required fields valid)         │   ║
║  └──────────────────────────────────────────────────────┘   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Session Timeout

```
╔══════════════════════════════════════════════════════════════╗
║                Session Expired                               ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║                    ⏱️ 🔒                                     ║
║                                                              ║
║              Your Session Has Expired                        ║
║                                                              ║
║      For your security, we've logged you out after           ║
║      30 minutes of inactivity.                               ║
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │ Don't worry! Your work has been saved.                 │ ║
║  │ Log back in to continue.                               │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  ┌──────────────────────────────────────────────────────┐   ║
║  │              [Log In Again]                          │   ║
║  │            (Primary #6366F1)                         │   ║
║  └──────────────────────────────────────────────────────┘   ║
║                                                              ║
║                   [Go to Home Page]                          ║
║                                                              ║
║  💾 Auto-saved content:                                      ║
║  • Draft outfit: "Summer Beach Look"                         ║
║  • Unsaved preferences                                       ║
║  • Shopping cart (5 items)                                   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Payment Declined

```
╔══════════════════════════════════════════════════════════════╗
║              Payment Declined                                ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║                    💳 ❌                                     ║
║                                                              ║
║              Payment Could Not Be Processed                  ║
║                                                              ║
║  Your payment was declined. Please try another payment       ║
║  method or contact your bank for more information.           ║
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │ Decline Reason: Insufficient Funds                     │ ║
║  │ Transaction ID: TXN-2025-10-16-5678                    │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  Order Summary: $323.98                                      ║
║  • 5 items in cart                                           ║
║  • Order #12345 - Reserved for 15 minutes                    ║
║                                                              ║
║  ┌──────────────────────────────────────────────────────┐   ║
║  │       [Try Different Payment Method]                 │   ║
║  │            (Primary #6366F1)                         │   ║
║  └──────────────────────────────────────────────────────┘   ║
║                                                              ║
║  Alternative options:                                        ║
║  [💳 Use Different Card] [🏦 Bank Transfer]                 ║
║  [💰 PayPal] [📱 Apple Pay]                                 ║
║                                                              ║
║              [Edit Order] [Contact Support]                  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

## ✅ Success & Confirmation States

### Order Confirmation

```
╔══════════════════════════════════════════════════════════════╗
║              Order Confirmed! 🎉                             ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║                    ✅                                        ║
║              (Animated checkmark)                            ║
║          (Scale + fade in animation)                         ║
║                                                              ║
║            Thank you for your order!                         ║
║                                                              ║
║  Order #12345 is confirmed and being processed               ║
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │ 📧 Confirmation sent to: sarah@email.com               │ ║
║  │ 📦 Estimated delivery: Oct 20-22, 2025                 │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  Order Summary:                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │ 5 items                              $323.98           │ ║
║  │ • White T-Shirt                      $29.99            │ ║
║  │ • Blue Jeans                         $49.99            │ ║
║  │ • [+ 3 more items]                                     │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  ┌──────────────────────────────────────────────────────┐   ║
║  │         [Track Your Order 📍]                        │   ║
║  │            (Primary #6366F1)                         │   ║
║  └──────────────────────────────────────────────────────┘   ║
║                                                              ║
║    [View Order Details] [Continue Shopping] [Share 📤]      ║
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │ 💡 What's Next?                                        │ ║
║  │ • We'll send tracking info when it ships               │ ║
║  │ • Questions? Contact customer support                  │ ║
║  │ • Share your outfit when it arrives! #CuratorAI        │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Item Added to Wardrobe

```
╔══════════════════════════════════════════════════════════════╗
║             Toast Notification (Bottom)                      ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  [Main content continues...]                                 ║
║                                                              ║
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │ ✓  Added to Wardrobe!                          [Undo] │ ║
║  │ (Slides up from bottom, auto-dismiss in 4s)            │ ║
║  │ (Green #10B981 bg, white text)                         │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  Animation:                                                  ║
║  1. Slide up from bottom (300ms ease-out)                    ║
║  2. Stay visible (4000ms)                                    ║
║  3. Progress bar depletes (4000ms linear)                    ║
║  4. Slide down to dismiss (300ms ease-in)                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Undo Action Confirmation

```
╔══════════════════════════════════════════════════════════════╗
║              Undo Action Pattern                             ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  User deletes item from wardrobe                             ║
║                    ↓                                         ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │ Item deleted                                    [Undo] │ ║
║  │ ████████░░░░░░░░ 5s remaining                          │ ║
║  │ (Orange #F59E0B bg, progress bar depletes)             │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  If user taps [Undo]:                                        ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │ ✓ Item restored!                                       │ ║
║  │ (Green #10B981 bg, brief appearance)                   │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  If timer expires:                                           ║
║  Item permanently deleted (moved to trash for 30 days)       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 👤 Profile & User Features

### User Profile View (Public)

```
╔══════════════════════════════════════════════════════════════╗
║ [← Back]          @fashionista            [•••]              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │               [Cover Photo]                            │ ║
║  │          (Gradient or image - 200px)                   │ ║
║  └────────────────────────────────────────────────────────┘ ║
║      ┌──────────┐                                            ║
║      │  [👤]    │  Sarah Martinez                            ║
║      │  Avatar  │  @fashionista                              ║
║      └──────────┘  Fashion Content Creator ✨                ║
║                                                              ║
║  ┌────────┐ ┌────────┐ ┌────────┐                          ║
║  │ 1,234  │ │  567   │ │  89    │                          ║
║  │  Posts │ │Followers│ │Following│                         ║
║  └────────┘ └────────┘ └────────┘                          ║
║                                                              ║
║  Fashion lover 👗 | NYC 📍 | Sharing daily outfit inspo     ║
║  🔗 www.fashionista.com                                      ║
║                                                              ║
║  ┌─────────────────┐  ┌─────────────────┐  [💬]           ║
║  │  [Follow +]     │  │  [Message]      │  More            ║
║  │  (Primary)      │  │  (Secondary)    │                  ║
║  └─────────────────┘  └─────────────────┘                  ║
║                                                              ║
║  [Grid 📷] [Lookbooks 📚] [Tagged 🏷] [Saved 🔖]           ║
║  (Tabs - Active: #6366F1)                                   ║
║  ═══════════                                                 ║
║                                                              ║
║  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐             ║
║  │[Img] │ │[Img] │ │[Img] │ │[Img] │ │[Img] │             ║
║  │ Post │ │ Post │ │ Post │ │ Post │ │ Post │             ║
║  │ ❤️234 │ │ ❤️567 │ │ ❤️890 │ │ ❤️123 │ │ ❤️456 │         ║
║  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘             ║
║                                                              ║
║  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐             ║
║  │[More posts in 3-column grid...]                          ║
║  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Edit Profile

```
╔══════════════════════════════════════════════════════════════╗
║ [✕]                 Edit Profile                  [Save]    ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │          [Cover Photo - Edit Overlay]                  │ ║
║  │              [📷 Change Cover]                         │ ║
║  └────────────────────────────────────────────────────────┘ ║
║      ┌──────────┐                                            ║
║      │  [👤]    │  [📷 Change]                               ║
║      │  Avatar  │                                            ║
║      └──────────┘                                            ║
║                                                              ║
║  ┌──────────────────────────────────────────────────────┐   ║
║  │ Name                                                 │   ║
║  │ [Sarah Martinez______]                               │   ║
║  └──────────────────────────────────────────────────────┘   ║
║                                                              ║
║  ┌──────────────────────────────────────────────────────┐   ║
║  │ Username                                             │   ║
║  │ [@fashionista________] ✓ Available                  │   ║
║  └──────────────────────────────────────────────────────┘   ║
║                                                              ║
║  ┌──────────────────────────────────────────────────────┐   ║
║  │ Bio (150 characters)                       89 left   │   ║
║  │ [Fashion lover 👗 | NYC 📍 | Sharing...____]         │   ║
║  │                                                      │   ║
║  │ [😊 Add Emoji]                                       │   ║
║  └──────────────────────────────────────────────────────┘   ║
║                                                              ║
║  ┌──────────────────────────────────────────────────────┐   ║
║  │ Website                                              │   ║
║  │ [https://www.fashionista.com____]                    │   ║
║  └──────────────────────────────────────────────────────┘   ║
║                                                              ║
║  ┌──────────────────────────────────────────────────────┐   ║
║  │ Location                                             │   ║
║  │ [🌍 New York, NY ▼]                                  │   ║
║  └──────────────────────────────────────────────────────┘   ║
║                                                              ║
║  Profile Privacy:                                            ║
║  ⚫ Public profile  ⚪ Private profile                       ║
║                                                              ║
║  [Advanced Settings →]                                       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Following/Followers List

```
╔══════════════════════════════════════════════════════════════╗
║ [← Back]              Followers                              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  [Followers (567)] [Following (89)]                          ║
║  ══════════════                                              ║
║                                                              ║
║  [🔍 Search followers...]                                    ║
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │ [👤] @username1              [Following ✓] [Message] │ ║
║  │      Sarah Johnson                                     │ ║
║  │      Fashion enthusiast • 234 posts                    │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │ [👤] @stylequeen             [Follow +]    [Remove]   │ ║
║  │      Emily Davis                                       │ ║
║  │      Style blogger • 567 posts                         │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │ [👤] @fashionlover           [Following ✓] [Message] │ ║
║  │      Michael Chen                                      │ ║
║  │      Menswear expert • 123 posts                       │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  Suggested for you:                                          ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │ [👤] @newcreator             [Follow +]               │ ║
║  │      Lisa Wong                                         │ ║
║  │      Rising fashion creator • Followed by 3 friends    │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  [Load More ↓]                                               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Block/Report User

```
╔══════════════════════════════════════════════════════════════╗
║  [✕]              Report User                                ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Why are you reporting @username?                            ║
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │ ⚪ Spam or misleading                                   │ ║
║  │    Commercial content or fake accounts                 │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │ ⚪ Harassment or bullying                               │ ║
║  │    Targeting someone with abuse                        │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │ ⚪ Inappropriate content                                │ ║
║  │    Violence, nudity, or sensitive content              │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │ ⚪ Intellectual property violation                      │ ║
║  │    Using copyrighted content without permission        │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │ ⚪ Something else                                       │ ║
║  │    Other issue not listed above                        │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  Additional details (optional):                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │ [Provide more context...                          ]   │ ║
║  │                                                        │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  [✓] Block this user                                         ║
║                                                              ║
║  ┌──────────────────────────────────────────────────────┐   ║
║  │              [Submit Report]                         │   ║
║  │            (Primary #6366F1)                         │   ║
║  └──────────────────────────────────────────────────────┘   ║
║                                                              ║
║  Your report is anonymous. We'll review it within 24 hours.  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 📊 Order History & Tracking

### Order History

```
╔══════════════════════════════════════════════════════════════╗
║ [👔 Logo]           Order History              [Filter ▼]   ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Your Orders                                                 ║
║                                                              ║
║  [All Orders] [In Progress] [Delivered] [Cancelled]          ║
║  ═══════════                                                 ║
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │ Order #12345                     🟢 In Transit         │ ║
║  │ Placed: Oct 16, 2025  •  Total: $323.98               │ ║
║  │                                                        │ ║
║  │ [Thumb] [Thumb] [Thumb] +2 more                        │ ║
║  │                                                        │ ║
║  │ Estimated delivery: Oct 20-22                          │ ║
║  │ ▰▰▰▰▰▰▰░░░ 70% complete                               │ ║
║  │                                                        │ ║
║  │ [Track Order 📍] [View Details →]                     │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │ Order #12344                     ✅ Delivered          │ ║
║  │ Placed: Oct 10, 2025  •  Total: $189.99               │ ║
║  │                                                        │ ║
║  │ [Thumb] [Thumb]                                        │ ║
║  │                                                        │ ║
║  │ Delivered: Oct 14, 2025                                │ ║
║  │                                                        │ ║
║  │ [Review Items ⭐] [Buy Again] [View Details →]        │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │ Order #12343                     ⚠️ Cancelled          │ ║
║  │ Placed: Oct 5, 2025   •  Refund: $99.99               │ ║
║  │                                                        │ ║
║  │ Cancelled at your request                              │ ║
║  │ Refund processed: Oct 6, 2025                          │ ║
║  │                                                        │ ║
║  │ [View Details →]                                       │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  [Load More Orders ↓]                                        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Live Order Tracking

```
╔══════════════════════════════════════════════════════════════╗
║ [← Back]           Track Order #12345                       ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │                   [Map View]                           │ ║
║  │         (Interactive map with delivery route)          │ ║
║  │                                                        │ ║
║  │     📍You            🚚 ----→                          │ ║
║  │     NYC                    📦 Warehouse                │ ║
║  │                                                        │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  Estimated delivery: Tomorrow, Oct 17 by 8 PM                ║
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │ ✅ Order Placed                      Oct 16, 10:30 AM │ ║
║  │    Order confirmed and payment processed               │ ║
║  │    ┃                                                   │ ║
║  │ ✅ Processing                        Oct 16, 2:15 PM  │ ║
║  │    Items picked and packed                             │ ║
║  │    ┃                                                   │ ║
║  │ ✅ Shipped                           Oct 16, 6:45 PM  │ ║
║  │    Package handed to carrier                           │ ║
║  │    Tracking: TRK-2025-10-16-1234                       │ ║
║  │    ┃                                                   │ ║
║  │ 🔵 In Transit                        Oct 17, 8:00 AM  │ ║
║  │    Out for delivery                                    │ ║
║  │    ┃ (Animated pulse)                                  │ ║
║  │ ⏸️  Arriving Soon                    Oct 17 (Est.)    │ ║
║  │    Expected between 6-8 PM                             │ ║
║  │    ┃                                                   │ ║
║  │ ⏸️  Delivered                        Pending           │ ║
║  │    Signature required                                  │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  Delivery Details:                                           ║
║  📦 Carrier: UPS                                             ║
║  📍 Destination: 123 Fashion Ave, New York, NY 10001         ║
║  📞 Contact: +1 (555) 123-4567                               ║
║                                                              ║
║  [🔔 Notify Me] [📞 Contact Courier] [Report Issue]         ║
║                                                              ║
║  Order Items (5):                                            ║
║  [Thumb] [Thumb] [Thumb] [+ View All]                       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 💬 Direct Messages

### Message List

```
╔══════════════════════════════════════════════════════════════╗
║ [← Back]              Messages              [✏️ New]         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  [🔍 Search messages...]                                     ║
║                                                              ║
║  [Primary 💬] [General 📁] [Unread Only (3)]                ║
║  ═════════                                                   ║
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │ [👤] @fashionista                          🔴 Online   │ ║
║  │      Hey! Love your recent outfit post! 😍             │ ║
║  │      2m ago  •  [1]                                    │ ║
║  │ (Unread badge - #EF4444, preview text - #6B7280)      │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │ [👤] @styleguru                            ⚪ 5h ago   │ ║
║  │      You: Thanks! Check out my lookbook 📚             │ ║
║  │      5h ago  •  ✓✓ Read                                │ ║
║  │ (Read receipt - #10B981)                               │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │ [👤] @fashionlover                         ⚪ 1d ago   │ ║
║  │      🖼️ Photo                                          │ ║
║  │      1d ago  •  [2]                                    │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │ [👤] @styleexpert                          ⚪ 3d ago   │ ║
║  │      You: See you at the fashion show! 👗              │ ║
║  │      3d ago  •  ✓ Sent                                 │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  [Load More Conversations ↓]                                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Message Thread

```
╔══════════════════════════════════════════════════════════════╗
║ [← Back]   [👤] @fashionista  🔴 Online       [📞] [•••]    ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║           Yesterday, Oct 15                                  ║
║                                                              ║
║                          ┌─────────────────────────┐         ║
║                          │ Hey! How are you? 😊    │         ║
║                          │ 10:30 AM  ✓✓           │         ║
║                          └─────────────────────────┘         ║
║                     (Sender bubble - #EEF2FF, right aligned) ║
║                                                              ║
║  ┌─────────────────────────┐                                ║
║  │ Great! Just posted      │                                ║
║  │ a new outfit 👗         │                                ║
║  │ 10:32 AM                │                                ║
║  └─────────────────────────┘                                ║
║  (Receiver bubble - #F3F4F6, left aligned)                   ║
║                                                              ║
║                          ┌─────────────────────────┐         ║
║                          │ Saw it! Love the style! │         ║
║                          │ Where did you get that  │         ║
║                          │ dress? 😍               │         ║
║                          │ 10:33 AM  ✓             │         ║
║                          └─────────────────────────┘         ║
║                                                              ║
║  ┌─────────────────────────┐                                ║
║  │ [🖼️ Image Preview]      │                                ║
║  │                         │                                ║
║  │ From my lookbook!       │                                ║
║  │ Link: zara.com/...      │                                ║
║  │ 10:35 AM                │                                ║
║  └─────────────────────────┘                                ║
║                                                              ║
║           Today, Oct 16                                      ║
║                                                              ║
║  ┌─────────────────────────┐                                ║
║  │ @fashionista is typing... ⋯                              │ ║
║  │ (Animated dots - #6B7280)                                │ ║
║  └─────────────────────────┘                                ║
║                                                              ║
║  ╔════════════════════════════════════════════════════════╗ ║
║  ║ [😊] [Type a message...]              [🖼️] [📎] [🎤] ║ ║
║  ║ (Input bar - fixed bottom, #FFFFFF bg, #E5E7EB border) ║ ║
║  ╚════════════════════════════════════════════════════════╝ ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 🎓 Onboarding Tutorial

### Style Quiz Onboarding

```
╔══════════════════════════════════════════════════════════════╗
║  [Skip]         Let's Find Your Style!         [Step 1 of 5]║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ●○○○○ Progress                                              ║
║  (Progress dots - Active: #6366F1, Inactive: #E5E7EB)       ║
║                                                              ║
║                What's your go-to style? 👔                   ║
║                                                              ║
║  Choose all that describe you:                               ║
║                                                              ║
║  ┌──────────────────┐  ┌──────────────────┐                ║
║  │                  │  │                  │                ║
║  │  [Image]         │  │  [Image]         │                ║
║  │  Casual & Comfy  │  │  Professional    │                ║
║  │                  │  │                  │                ║
║  │  [✓ Selected]    │  │  [Not Selected]  │                ║
║  └──────────────────┘  └──────────────────┘                ║
║  (#6366F1 border)      (#E5E7EB border)                     ║
║                                                              ║
║  ┌──────────────────┐  ┌──────────────────┐                ║
║  │  [Image]         │  │  [Image]         │                ║
║  │  Street Style    │  │  Bohemian        │                ║
║  │  [Not Selected]  │  │  [✓ Selected]    │                ║
║  └──────────────────┘  └──────────────────┘                ║
║                                                              ║
║  ┌──────────────────┐  ┌──────────────────┐                ║
║  │  [Image]         │  │  [Image]         │                ║
║  │  Minimal         │  │  Vintage         │                ║
║  │  [Not Selected]  │  │  [Not Selected]  │                ║
║  └──────────────────┘  └──────────────────┘                ║
║                                                              ║
║  Selected: 2 styles                                          ║
║                                                              ║
║  ┌──────────────────────────────────────────────────────┐   ║
║  │              [Continue →]                            │   ║
║  │      (Primary #6366F1, enabled when ≥1 selected)     │   ║
║  └──────────────────────────────────────────────────────┘   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Feature Walkthrough

```
╔══════════════════════════════════════════════════════════════╗
║              Welcome Tutorial Overlay                        ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  [Darkened background with spotlight on feature]             ║
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │                                                        │ ║
║  │            [Highlighted Feature Area]                  │ ║
║  │         (Normal brightness, rest dimmed)               │ ║
║  │                                                        │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                     ↓                                        ║
║              ┌─────────────────────────────────┐            ║
║              │  📸 Upload Your First Photo     │            ║
║              │                                 │            ║
║              │  Tap here to upload an outfit   │            ║
║              │  photo and get instant style    │            ║
║              │  recommendations!               │            ║
║              │                                 │            ║
║              │  [Got It!]  [1/5]  [Next →]   │            ║
║              └─────────────────────────────────┘            ║
║              (Tooltip - #FFFFFF, shadow Level 3)            ║
║                                                              ║
║  [Skip Tutorial]                                             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 🎨 Micro-interactions & Animations

### Button Hover States

```
╔══════════════════════════════════════════════════════════════╗
║            Button State Transitions                          ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Primary Button:                                             ║
║                                                              ║
║  Default:                                                    ║
║  ┌──────────────┐                                            ║
║  │  Click Me!   │  #6366F1 bg, #FFFFFF text                 ║
║  └──────────────┘  Shadow: Level 1                          ║
║                                                              ║
║  Hover:                                                      ║
║  ┌──────────────┐                                            ║
║  │  Click Me!   │  #4F46E5 bg (darker)                      ║
║  └──────────────┘  Shadow: Level 2                          ║
║  (Transform: scale(1.02), Duration: 200ms)                   ║
║                                                              ║
║  Active (Click):                                             ║
║  ┌──────────────┐                                            ║
║  │  Click Me!   │  #4338CA bg (darkest)                     ║
║  └──────────────┘  Shadow: Level 0                          ║
║  (Transform: scale(0.98), Duration: 100ms)                   ║
║  (Haptic feedback on mobile)                                 ║
║                                                              ║
║  Loading:                                                    ║
║  ┌──────────────┐                                            ║
║  │  ⟳ Loading...│  Spinner animation, text fades 50%        ║
║  └──────────────┘  Cursor: not-allowed                      ║
║                                                              ║
║  Success:                                                    ║
║  ┌──────────────┐                                            ║
║  │  ✓ Done!     │  #10B981 bg, brief (800ms)               ║
║  └──────────────┘  Scale pulse: 1→1.05→1                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Like Animation Sequence

```
╔══════════════════════════════════════════════════════════════╗
║              Like Button Animation                           ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Frame 1 (0ms): Default                                      ║
║  ┌────┐                                                      ║
║  │ ♡  │  #6B7280 (gray outline)                             ║
║  └────┘  234 likes                                           ║
║                                                              ║
║  Frame 2 (0-100ms): Click                                    ║
║  ┌────┐                                                      ║
║  │ ♡→ │  Start fill animation                                ║
║  └────┘  Scale: 1→0.8                                        ║
║                                                              ║
║  Frame 3 (100-200ms): Fill                                   ║
║  ┌────┐                                                      ║
║  │ ❤️  │  #EF4444 (red fill)                                ║
║  └────┘  Scale: 0.8→1.2                                      ║
║          Particle burst (8 hearts)                           ║
║                                                              ║
║  Frame 4 (200-300ms): Settle                                 ║
║  ┌────┐                                                      ║
║  │ ❤️  │  Scale: 1.2→1.0 (spring ease)                      ║
║  └────┘  235 (number increments)                             ║
║          Haptic feedback pulse                               ║
║                                                              ║
║  Frame 5 (300ms+): Complete                                  ║
║  ┌────┐                                                      ║
║  │ ❤️  │  Stable state                                       ║
║  └────┘  235 likes                                           ║
║                                                              ║
║  Unlike (reverse animation): ❤️ → ♡                         ║
║  Duration: 200ms, no particles                               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Card Hover Effect

```
╔══════════════════════════════════════════════════════════════╗
║              Card Hover Interactions                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Outfit Card - Default:                                      ║
║  ┌──────────────────┐                                        ║
║  │                  │                                        ║
║  │  [Outfit Image]  │  Shadow: Level 1                       ║
║  │                  │  Transform: none                       ║
║  │  Summer Vibes 🌞 │  Border: 1px #E5E7EB                  ║
║  │  $89-$145        │                                        ║
║  │  ❤️ 💾 ↗         │  Icons: #6B7280                       ║
║  └──────────────────┘                                        ║
║                                                              ║
║  On Hover:                                                   ║
║  ┌──────────────────┐                                        ║
║  │                  │  ↑ Lifts up                            ║
║  │  [Outfit Image]  │  Shadow: Level 3                       ║
║  │   [Quick View]   │  Transform: translateY(-4px)           ║
║  │  Summer Vibes 🌞 │  Border: 2px #6366F1                  ║
║  │  $89-$145        │  Duration: 300ms                       ║
║  │  ❤️ 💾 ↗         │  Icons: #6366F1 (colorize)            ║
║  └──────────────────┘  Image: brightness(1.05)               ║
║                                                              ║
║  Overlay appears:                                            ║
║  • "Quick View" button fades in (0→1 opacity, 200ms)         ║
║  • Action icons scale up slightly (1→1.1)                    ║
║  • Image zooms subtly (scale: 1→1.05)                        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 📱 Touch Gestures Guide

```
╔══════════════════════════════════════════════════════════════╗
║              Mobile Gesture Library                          ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  TAP                                                         ║
║  👆 Single tap → Select, open, activate                      ║
║  Context: All tappable elements                              ║
║  Feedback: Visual state change + optional haptic             ║
║                                                              ║
║  DOUBLE TAP                                                  ║
║  👆👆 Quick double tap → Like, zoom                          ║
║  Context: Posts, images                                      ║
║  Feedback: Heart animation + haptic pulse                    ║
║                                                              ║
║  LONG PRESS                                                  ║
║  👆🕐 Press & hold (500ms) → Context menu                    ║
║  Context: Cards, items, messages                             ║
║  Feedback: Haptic on trigger, menu appears, subtle scale     ║
║                                                              ║
║  SWIPE RIGHT                                                 ║
║  👉 Swipe right → Quick like, go back                        ║
║  Context: Posts, navigation                                  ║
║  Feedback: Icon slides in, haptic on complete                ║
║                                                              ║
║  SWIPE LEFT                                                  ║
║  👈 Swipe left → Actions menu, archive                       ║
║  Context: Lists, messages, notifications                     ║
║  Feedback: Actions reveal with spring, haptic on reveal      ║
║                                                              ║
║  SWIPE UP                                                    ║
║  👆 Swipe up → Next item, close modal                        ║
║  Context: Stories, bottom sheets                             ║
║  Feedback: Smooth transition, momentum                       ║
║                                                              ║
║  SWIPE DOWN                                                  ║
║  👇 Swipe down → Refresh, dismiss, previous                  ║
║  Context: Feeds, modals                                      ║
║  Feedback: Pull indicator, haptic on trigger                 ║
║                                                              ║
║  PINCH                                                       ║
║  👌 Pinch in/out → Zoom                                      ║
║  Context: Images, maps                                       ║
║  Feedback: Smooth scaling, momentum                          ║
║                                                              ║
║  DRAG                                                        ║
║  ✊ Press & drag → Reorder, move                             ║
║  Context: Lists, outfit creator                              ║
║  Feedback: Shadow increases, haptic on drop                  ║
║                                                              ║
║  TWO-FINGER SWIPE                                            ║
║  👆👆 Two fingers → Navigate back                            ║
║  Context: Navigation                                         ║
║  Feedback: Page slides with momentum                         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 🎯 Accessibility Features

### Screen Reader Optimization

```
╔══════════════════════════════════════════════════════════════╗
║          Accessibility Implementation Guide                  ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ARIA LABELS & ROLES                                         ║
║                                                              ║
║  <button aria-label="Like this outfit"                       ║
║          role="button"                                       ║
║          aria-pressed="false">                               ║
║    ❤️                                                        ║
║  </button>                                                   ║
║                                                              ║
║  <img src="outfit.jpg"                                       ║
║       alt="Blue summer dress with white sneakers,            ║
║            casual style, perfect for beach days"             ║
║       role="img">                                            ║
║                                                              ║
║  FOCUS INDICATORS                                            ║
║  ┌─────────────────────┐                                    ║
║  │  [Button Text]      │                                    ║
║  └─────────────────────┘                                    ║
║  (Default - no outline)                                      ║
║                                                              ║
║  ┌─────────────────────┐                                    ║
║  ║  [Button Text]      ║  ← 3px #6366F1 outline            ║
║  └─────────────────────┘     4px offset                     ║
║  (Focused - visible outline)                                 ║
║                                                              ║
║  KEYBOARD NAVIGATION                                         ║
║  • Tab: Move to next focusable element                       ║
║  • Shift+Tab: Move to previous element                       ║
║  • Enter/Space: Activate buttons                             ║
║  • Arrow keys: Navigate within components                    ║
║  • Escape: Close modals/menus                                ║
║                                                              ║
║  SKIP LINKS                                                  ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │ [Skip to main content] [Skip to navigation]            │ ║
║  │ (Visible only on focus, top of page)                   │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  COLOR CONTRAST                                              ║
║  • Text: Minimum 4.5:1 ratio (WCAG AA)                       ║
║  • Large text: Minimum 3:1 ratio                             ║
║  • Interactive elements: 3:1 ratio                           ║
║  • High contrast mode toggle available                       ║
║                                                              ║
║  TOUCH TARGET SIZES                                          ║
║  Minimum: 44x44px (iOS) / 48x48dp (Android)                  ║
║  Recommended: 48x48px across all platforms                   ║
║                                                              ║
║  ANNOUNCEMENTS                                               ║
║  <div role="status"                                          ║
║       aria-live="polite"                                     ║
║       aria-atomic="true">                                    ║
║    Item added to wardrobe                                    ║
║  </div>                                                      ║
║                                                              ║
║  REDUCED MOTION                                              ║
║  @media (prefers-reduced-motion: reduce) {                   ║
║    * { animation-duration: 0.01ms !important; }              ║
║  }                                                           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 📊 Admin Analytics Detailed

### Analytics Dashboard

```
╔══════════════════════════════════════════════════════════════╗
║ [👔 Logo]      Analytics & Insights           [Export 📊]   ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  [Overview] [Users] [Engagement] [Revenue] [AI Metrics]     ║
║  ══════════                                                  ║
║                                                              ║
║  Date Range: [Last 30 Days ▼]  [Custom Range]  [Compare ⚖] ║
║                                                              ║
║  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐              ║
║  │ 12,453 │ │ 45.2k  │ │  89%   │ │  2.4m  │              ║
║  │  Users │ │ Revenue│ │  Conv. │ │  Views │              ║
║  │  +12%↗ │ │ +18%↗  │ │  +2%↗  │ │  +25%↗ │              ║
║  └────────┘ └────────┘ └────────┘ └────────┘              ║
║                                                              ║
║  User Growth Trend                                           ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │ 15k│                                          ╱╱╱      │ ║
║  │    │                                      ╱╱╱╱         │ ║
║  │ 10k│                              ╱╱╱╱╱╱╱              │ ║
║  │    │                      ╱╱╱╱╱╱╱╱                     │ ║
║  │  5k│              ╱╱╱╱╱╱╱╱                             │ ║
║  │    │      ╱╱╱╱╱╱╱╱                                     │ ║
║  │  0 ├──────────────────────────────────────────────────│ ║
║  │    Jan  Feb  Mar  Apr  May  Jun  Jul  Aug  Sep  Oct   │ ║
║  │    (Line chart - #6366F1, gradient fill)              │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  Engagement Metrics                                          ║
║  ┌──────────────────┐  ┌──────────────────┐               ║
║  │ Avg. Session     │  │ Bounce Rate      │               ║
║  │ 12m 34s          │  │ 32.5%            │               ║
║  │ +2m 15s ↗        │  │ -5.2% ↘          │               ║
║  └──────────────────┘  └──────────────────┘               ║
║                                                              ║
║  Top Performing Content                                      ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │ 1. Summer Lookbook                 12.3k views  ↗123%│ ║
║  │ 2. Street Style Guide               8.9k views  ↗89% │ ║
║  │ 3. Office Outfit Ideas              6.7k views  ↗67% │ ║
║  │ 4. Weekend Casual Collection        5.4k views  ↗54% │ ║
║  │ 5. Date Night Outfits               4.2k views  ↗42% │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  [View Detailed Report →]  [Schedule Email Report]          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 🌍 Responsive Breakpoint Examples

### Mobile (375px)

```
┌─────────────────────────┐
│ [☰] CuratorAI    [🔔][👤]│
├─────────────────────────┤
│                         │
│  [Full-width card]      │
│  ┌─────────────────────┐│
│  │                     ││
│  │   Outfit Image      ││
│  │                     ││
│  ├─────────────────────┤│
│  │ Title & Details     ││
│  │ ❤️ 💾 ↗             ││
│  └─────────────────────┘│
│                         │
│  [Full-width card]      │
│  [Full-width card]      │
│                         │
├─────────────────────────┤
│ [🏠][🔍][➕][👕][👤]   │
└─────────────────────────┘
Single column, stacked
Bottom navigation
```

### Tablet (768px)

```
┌───────────────────────────────────────────┐
│ [☰] CuratorAI  [🔍Search]  [🔔] [👤]     │
├───────────────────────────────────────────┤
│                                           │
│  ┌────────────┐  ┌────────────┐          │
│  │   Card 1   │  │   Card 2   │          │
│  │   Image    │  │   Image    │          │
│  └────────────┘  └────────────┘          │
│                                           │
│  ┌────────────┐  ┌────────────┐          │
│  │   Card 3   │  │   Card 4   │          │
│  └────────────┘  └────────────┘          │
│                                           │
└───────────────────────────────────────────┘
Two columns, top navigation
Hamburger menu for sidebar
```

### Desktop (1440px)

```
┌─────────────────────────────────────────────────────────┐
│ [👔 Logo]  [🔍 Search bar]          [🔔] [👤 Profile▼]│
├───────────┬─────────────────────────────────────────────┤
│ Sidebar   │              Main Content                   │
│ ┌───────┐ │  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  │
│ │ Home  │ │  │ Card │  │ Card │  │ Card │  │ Card │  │
│ │ Search│ │  └──────┘  └──────┘  └──────┘  └──────┘  │
│ │Wardrobe│ │                                           │
│ │ Feed  │ │  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  │
│ │Settings│ │  │ Card │  │ Card │  │ Card │  │ Card │  │
│ └───────┘ │  └──────┘  └──────┘  └──────┘  └──────┘  │
└───────────┴─────────────────────────────────────────────┘
Four columns, persistent sidebar
Expanded navigation
```

---

**🎉 End of Wireframes**


Total screens: **40+ comprehensive wireframes** covering every aspect of the CuratorAI MVP!