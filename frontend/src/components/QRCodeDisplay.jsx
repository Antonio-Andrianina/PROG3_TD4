import { QRCodeSVG } from "qrcode.react";

export default function QRCodeDisplay({ value }) {
    if (!value) return null;

    return (
        <div className="flex flex-col items-center gap-4 mt-6">
            <h2 className="text-white text-xl">
                Scanner avec le wallet
            </h2>

            <div className="bg-white p-4 rounded-xl">
                <QRCodeSVG
                    value={value}
                    size={250}
                />
            </div>
        </div>
    );
}