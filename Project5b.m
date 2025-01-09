clear, clc, close all

% parameters
cr = 0.01;               % Rolweerstandscoëfficiënt
m = 70;                  % Massa van de fietser + fiets (kg)
g = 9.81;                % Gravitatieversnelling (m/s^2)
cd = 0.9;                % Luchtweerstandscoëfficiënt
rho_air = 1.225;         % Dichtheid van lucht (kg/m^3)
A = 0.5;                 % Frontale oppervlakte (m^2)
vwind = 2;               % Windsnelheid (m/s)
alpha = 5 * pi / 180;    % Hellinghoek (graden naar radialen)
v = 10;                  % Snelheid van de fietser (m/s)
a = 0.5;                 % Versnelling (m/s^2)

% Bereken de individuele vermogens
Proll = cr * m * g * cos(alpha) * v;                     % Rolweerstand
Pdrag = 0.5 * cd * rho_air * A * (v - vwind)^2 * v;     % Luchtweerstand
Pkinetic = m * v * a;                                   % Kinetische energie
Pgravitational = m * g * v * sin(alpha);                % Gravitatiekracht

% Totaal vermogen
Poutput = Proll + Pdrag + Pkinetic + Pgravitational;
Pinput = Poutput + Proll + Pdrag + Pkinetic + Pgravitational;

% Vermogenverliesvergelijking
loss_equation = Poutput - Pkinetic - Pgravitational - (Proll + Pdrag);

% Herschreven vergelijking
rewritten_equation = Poutput - m * v * a - m * g * v * sin(alpha) - ...
    (cr * m * g * v + 0.5 * cd * rho_air * A * (v - vwind)^2 * v);

% Samengevoegde vergelijking
combined_equation = Poutput - m * v * a - m * g * v * alpha - ...
    (cr * m * g * v + 0.5 * cd * rho_air * A * (v - vwind)^2 * v);

% Resultaten weergeven
fprintf('Proll: %.2f W\n', Proll);
fprintf('Pdrag: %.2f W\n', Pdrag);
fprintf('Pkinetic: %.2f W\n', Pkinetic);
fprintf('Pgravitational: %.2f W\n', Pgravitational);
fprintf('Poutput: %.2f W\n', Poutput);
fprintf('Pinput: %.2f W\n', Pinput);
fprintf('Loss equation result: %.2f W\n', loss_equation);
fprintf('Rewritten equation result: %.2f W\n', rewritten_equation);
fprintf('Combined equation result: %.2f W\n', combined_equation);
