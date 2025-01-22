from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def queue_calculator():
    result = None
    error = None
    steps = None

    if request.method == 'POST':
        try:
            # Mengambil data dari form
            interarrival_time = float(request.form['interarrival_time'])  # Waktu antar kedatangan (Ta)
            service_time = float(request.form['service_time'])  # Waktu pelayanan (Ts)

            # Validasi untuk nilai valid
            if interarrival_time <= 0 or service_time <= 0:
                error = "Waktu antar kedatangan dan waktu pelayanan harus lebih besar dari nol."
            else:
                # Perhitungan
                arrival_rate = 1 / interarrival_time  # λ (Laju kedatangan pelanggan)
                service_rate = 1 / service_time  # μ (Laju pelayanan per pelayan)
                rho = arrival_rate / (2 * service_rate)  # Pemanfaatan pelayan (ρ)

                # Validasi stabilitas sistem
                if rho >= 1:
                    error = "Peringatan: Sistem antrian di kafe tidak stabil karena pemanfaatan pelayan (ρ) ≥ 1."
                
                # Hitung waktu rata-rata dalam sistem dan antrian jika sistem stabil
                W = 1 / (service_rate - arrival_rate / 2) if rho < 1 else float('inf')  # Waktu rata-rata dalam sistem
                Wq = W - (1 / service_rate) if rho < 1 else float('inf')  # Waktu rata-rata dalam antrian

                # Hasil perhitungan
                result = {
                    'lambda': round(arrival_rate, 4),  # Laju kedatangan
                    'mu': round(service_rate, 4),  # Laju pelayanan
                    'rho': round(rho, 4),  # Pemanfaatan pelayan
                    'W': round(W, 4) if W != float('inf') else "Tak Terhingga",  # Waktu rata-rata dalam sistem
                    'Wq': round(Wq, 4) if Wq != float('inf') else "Tak Terhingga"  # Waktu rata-rata dalam antrian
                }

                # Langkah-langkah perhitungan (format MathJax)
                steps = f"""
                1. Laju Kedatangan Pelanggan (λ):
$$\\lambda = \\frac{{1}}{{T_a}} = \\frac{{1}}{{{interarrival_time}}} = {round(arrival_rate, 4)} \\text{{ pelanggan/menit}}$$

                2. Laju Pelayanan per Pelayan (μ):
$$\\mu = \\frac{{1}}{{T_s}} = \\frac{{1}}{{{service_time}}} = {round(service_rate, 4)} \\text{{ pelanggan/menit}}$$

                3. Pemanfaatan Pelayan (ρ):
$$\\rho = \\frac{{\\lambda}}{{2 \\mu}} = \\frac{{{round(arrival_rate, 4)}}}{{2 \\times {round(service_rate, 4)}}} = {round(rho, 4)}$$

                4. Waktu Rata-rata dalam Sistem (W):
$$W = \\frac{{1}}{{\\mu - \\frac{{\\lambda}}{{2}}}} = {round(W, 4) if W != float('inf') else "Tak Terhingga"} \\text{{ menit}}$$

                5. Waktu Rata-rata dalam Antrian (Wq):
$$W_q = W - \\frac{{1}}{{\\mu}} = {round(Wq, 4) if Wq != float('inf') else "Tak Terhingga"} \\text{{ menit}}$$
                """
        except Exception as e:
            error = f"Error: {e}"

    return render_template('index.html', result=result, error=error, steps=steps)


if __name__ == '__main__':
    app.run(debug=True)
